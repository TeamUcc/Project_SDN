#!/usr/bin/env python3
"""
ZeroTrust SDN Controller usando Ryu
Implementa microsegmentación, detección automática y respuesta a amenazas
"""

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, arp, tcp, udp
from ryu.app.wsgi import WSGIApplication, route, Response
from ryu.topology.api import get_switch, get_link
from ryu.topology import event as topo_event
import json
import yaml
import logging
import time
from datetime import datetime
from collections import defaultdict

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Constantes
ZERO_TRUST_API = 'zero_trust_api'
FLOW_IDLE_TIMEOUT = 60
FLOW_HARD_TIMEOUT = 300
DEFAULT_PRIORITY = 100
HIGH_PRIORITY = 1000

class ZeroTrustController(app_manager.RyuApp):
    """
    Controlador SDN con arquitectura Zero Trust
    """
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    _CONTEXTS = {'wsgi': WSGIApplication}

    def __init__(self, *args, **kwargs):
        super(ZeroTrustController, self).__init__(*args, **kwargs)
        
        # Configurar API REST
        wsgi = kwargs['wsgi']
        wsgi.register(ZeroTrustAPI, {ZERO_TRUST_API: self})
        
        # Estados del controlador
        self.mac_to_port = {}  # Switch -> {MAC -> Puerto}
        self.datapaths = {}    # Switch ID -> Datapath
        self.blocked_macs = set()  # MACs bloqueadas
        self.device_roles = {}     # MAC -> Rol
        self.quarantine = set()    # MACs en cuarentena
        
        # Estadísticas
        self.stats = {
            'packets_processed': 0,
            'flows_installed': 0,
            'blocked_attempts': 0,
            'alerts_received': 0
        }
        
        # Políticas Zero Trust
        self.load_policies()
        
        self.logger.info("🔒 ZeroTrust Controller iniciado")

    def load_policies(self):
        """Cargar políticas de seguridad desde archivo YAML"""
        try:
            with open('apps/config/policy.yaml', 'r') as f:
                config = yaml.safe_load(f)
                self.policies = config.get('policies', {})
                self.default_role = config.get('default_role', 'quarantine')
                self.logger.info(f"Políticas cargadas: {list(self.policies.keys())}")
        except FileNotFoundError:
            # Políticas por defecto si no existe archivo
            self.policies = {
                'students': {'allowed': ['servers', 'internet'], 'priority': 50},
                'servers': {'allowed': ['students', 'admin'], 'priority': 80},
                'admin': {'allowed': ['servers', 'students'], 'priority': 90},
                'guests': {'allowed': ['internet'], 'priority': 10},
                'quarantine': {'allowed': [], 'priority': 0}
            }
            self.default_role = 'quarantine'
            self.logger.warning("Usando políticas por defecto")

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        """Configurar switch cuando se conecta"""
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        self.datapaths[datapath.id] = datapath
        self.logger.info(f"Switch {datapath.id} conectado")

        # Instalar tabla por defecto: enviar al controlador
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                        ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions, table_id=0)
        
        # Instalar flujo de drop por defecto con prioridad muy baja
        self.add_drop_flow(datapath, priority=1)

    def add_flow(self, datapath, priority, match, actions, 
                 buffer_id=None, table_id=0, idle_timeout=FLOW_IDLE_TIMEOUT):
        """Instalar flujo en el switch"""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                  priority=priority, match=match,
                                  instructions=inst, table_id=table_id,
                                  idle_timeout=idle_timeout)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                  match=match, instructions=inst,
                                  table_id=table_id, idle_timeout=idle_timeout)
        
        datapath.send_msg(mod)
        self.stats['flows_installed'] += 1

    def add_drop_flow(self, datapath, match=None, priority=1, table_id=0):
        """Instalar flujo de drop"""
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        if match is None:
            match = parser.OFPMatch()
        
        # Sin acciones = drop
        inst = []
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                              match=match, instructions=inst, table_id=table_id)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        """Manejar paquetes que llegan al controlador"""
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        # Parsear paquete
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        
        if not eth_pkt:
            return

        # Ignorar paquetes LLDP
        if eth_pkt.ethertype == 0x88cc:
            return

        dst_mac = eth_pkt.dst
        src_mac = eth_pkt.src
        
        self.stats['packets_processed'] += 1

        # Aprender MAC -> Puerto
        self.mac_to_port.setdefault(datapath.id, {})
        self.mac_to_port[datapath.id][src_mac] = in_port

        # Verificar si la MAC está bloqueada
        if src_mac in self.blocked_macs:
            self.logger.warning(f"🚫 Paquete bloqueado de MAC: {src_mac}")
            self.stats['blocked_attempts'] += 1
            return


        # Asignar rol por defecto a nuevos dispositivos
        if src_mac not in self.device_roles:
            self.device_roles[src_mac] = self.default_role
            self.quarantine.add(src_mac)
            self.logger.info(f"🔍 Nuevo dispositivo en cuarentena: {src_mac}")

        # Verificar política Zero Trust
        if not self.check_zero_trust_policy(src_mac, dst_mac):
            self.logger.warning(f"🔒 Comunicación denegada: {src_mac} -> {dst_mac}")
            return

        # Determinar puerto de salida
        if dst_mac in self.mac_to_port[datapath.id]:
            out_port = self.mac_to_port[datapath.id][dst_mac]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # Instalar flujo para evitar PacketIn futuro
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst_mac, eth_src=src_mac)
            self.add_flow(datapath, DEFAULT_PRIORITY, match, actions)

        # Enviar paquete
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

    def check_zero_trust_policy(self, src_mac, dst_mac):
        """Verificar si la comunicación está permitida por política Zero Trust"""
        src_role = self.device_roles.get(src_mac, self.default_role)
        dst_role = self.device_roles.get(dst_mac, self.default_role)
        
        # Si está en cuarentena, solo permitir tráfico administrativo
        if src_mac in self.quarantine:
            return False
            
        # Verificar política
        src_policy = self.policies.get(src_role, {})
        allowed_roles = src_policy.get('allowed', [])
        
        return dst_role in allowed_roles or dst_mac == 'ff:ff:ff:ff:ff:ff'  # Permitir broadcast

    def block_device(self, mac_address):
        """Bloquear dispositivo por MAC"""
        self.blocked_macs.add(mac_address)
        
        # Instalar flujos de drop en todos los switches
        for dp_id, datapath in self.datapaths.items():
            parser = datapath.ofproto_parser
            
            # Bloquear tráfico de origen
            match_src = parser.OFPMatch(eth_src=mac_address)
            self.add_drop_flow(datapath, match_src, HIGH_PRIORITY)
            
            # Bloquear tráfico de destino
            match_dst = parser.OFPMatch(eth_dst=mac_address)
            self.add_drop_flow(datapath, match_dst, HIGH_PRIORITY)
        
        self.logger.warning(f"🚫 Dispositivo bloqueado: {mac_address}")

    def assign_role(self, mac_address, role):
        """Asignar rol a dispositivo"""
        if role in self.policies:
            self.device_roles[mac_address] = role
            self.quarantine.discard(mac_address)  # Sacar de cuarentena
            self.logger.info(f"👤 Rol asignado: {mac_address} -> {role}")
            return True
        return False

    def get_stats(self):
        """Obtener estadísticas del controlador"""
        stats = self.stats.copy()
        stats.update({
            'total_devices': len(self.device_roles),
            'blocked_devices': len(self.blocked_macs),
            'quarantined_devices': len(self.quarantine),
            'policies_loaded': len(self.policies),
            'switches_connected': len(self.datapaths)
        })
        return stats


class ZeroTrustAPI:
    """API REST para el controlador Zero Trust"""
    
    def __init__(self, req, link, data, **config):
        self.controller = data[ZERO_TRUST_API]

    @route('zt', '/stats', methods=['GET'])
    def get_stats(self, req, **kwargs):
        """Obtener estadísticas"""
        stats = self.controller.get_stats()
        return Response(content_type='application/json',
                       body=json.dumps(stats, indent=2))

    @route('zt', '/block/{mac}', methods=['POST'])
    def block_device(self, req, **kwargs):
        """Bloquear dispositivo por MAC"""
        mac = kwargs['mac']
        self.controller.block_device(mac)
        return Response(status=200, body=f'Device {mac} blocked\n')

    @route('zt', '/unblock/{mac}', methods=['POST'])
    def unblock_device(self, req, **kwargs):
        """Desbloquear dispositivo"""
        mac = kwargs['mac']
        self.controller.blocked_macs.discard(mac)
        return Response(status=200, body=f'Device {mac} unblocked\n')

    @route('zt', '/role/{mac}/{role}', methods=['POST'])
    def assign_role(self, req, **kwargs):
        """Asignar rol a dispositivo"""
        mac = kwargs['mac']
        role = kwargs['role']
        
        if self.controller.assign_role(mac, role):
            return Response(status=200, body=f'Role {role} assigned to {mac}\n')
        else:
            return Response(status=400, body=f'Invalid role: {role}\n')

    @route('zt', '/devices', methods=['GET'])
    def list_devices(self, req, **kwargs):
        """Listar dispositivos y sus roles"""
        devices = {}
        for mac, role in self.controller.device_roles.items():
            devices[mac] = {
                'role': role,
                'blocked': mac in self.controller.blocked_macs,
                'quarantined': mac in self.controller.quarantine
            }
        
        return Response(content_type='application/json',
                       body=json.dumps(devices, indent=2))

    @route('zt', '/policies', methods=['GET'])
    def get_policies(self, req, **kwargs):
        """Obtener políticas cargadas"""
        return Response(content_type='application/json',
                       body=json.dumps(self.controller.policies, indent=2))


if __name__ == '__main__':
    # Para ejecutar directamente
    from ryu.cmd import manager
    import sys
    
    sys.argv.append('apps.zero_trust_controller')
    sys.argv.append('--verbose')
    manager.main()