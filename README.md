# Project_SDN

# Guía Completa para Proyecto SDN - Redes de Computadores

## 1. Conceptos Fundamentales SDN

### ¿Qué es SDN?
- **Software-Defined Networking**: Arquitectura que separa el plano de control del plano de datos
- **Plano de Control**: Donde se toman decisiones de enrutamiento (Controlador)
- **Plano de Datos**: Donde se reenvían los paquetes (Switches OpenFlow)
- **Protocolo OpenFlow**: Comunicación entre controlador y switches

### Ventajas Clave
- Programabilidad de la red
- Gestión centralizada
- Flexibilidad y adaptabilidad
- Facilita la innovación y automatización

## 2. Herramientas y Software Necesarios

### Simulador de Red: Mininet
```bash
# Instalación en Ubuntu/Debian
sudo apt-get update
sudo apt-get install mininet
```

### Controlador SDN (Opciones)
1. **OpenDaylight** (Java) - Empresarial
2. **Floodlight** (Java) - Más simple
3. **Ryu** (Python) - Ideal para aprendizaje
4. **POX** (Python) - Educativo

### Recomendación: Empezar con Ryu
```bash
# Instalación de Ryu
pip install ryu
```

## 3. Arquitectura del Proyecto

### Topología Sugerida
```
    Controlador SDN (Ryu/POX)
           |
    OpenFlow Protocol
           |
    +------+------+------+
    |      |      |      |
   SW1    SW2    SW3    SW4
    |      |      |      |
   H1-H2  H3-H4  H5-H6  H7-H8
```

### Componentes
- **1 Controlador SDN**
- **4 Switches OpenFlow**
- **8 Hosts**
- **Conexiones redundantes para demostrar balanceo de carga**

## 4. Implementación Paso a Paso

### Paso 1: Crear Topología en Mininet
```python
# topo_basica.py
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI

class MiTopologia(Topo):
    def build(self):
        # Agregar switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        
        # Agregar hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        
        # Enlaces host-switch
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        
        # Enlaces entre switches
        self.addLink(s1, s3)
        self.addLink(s2, s3)
        self.addLink(s3, s4)

def ejecutar_red():
    topo = MiTopologia()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    ejecutar_red()
```

### Paso 2: Controlador Básico con Ryu
```python
# controlador_basico.py
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class ControladorBasico(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    
    def __init__(self, *args, **kwargs):
        super(ControladorBasico, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
    
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # Instalar regla por defecto
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                        ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
    
    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                           actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                               match=match, instructions=inst)
        datapath.send_msg(mod)
    
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        
        dst = eth.dst
        src = eth.src
        
        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        
        # Aprender la MAC del origen
        self.mac_to_port[dpid][src] = in_port
        
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD
        
        actions = [parser.OFPActionOutput(out_port)]
        
        # Instalar regla de flujo
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.add_flow(datapath, 1, match, actions)
        
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
        
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
```

### Paso 3: Ejecución del Proyecto
```bash
# Terminal 1: Iniciar controlador
ryu-manager controlador_basico.py

# Terminal 2: Iniciar topología
sudo python topo_basica.py
```

## 5. Funcionalidades Avanzadas para tu Proyecto

### A) Balanceador de Carga
- Implementar selección de rutas basada en carga de enlaces
- Monitorear estadísticas de tráfico
- Redistribuir flujos dinámicamente

### B) Firewall SDN
- Bloquear tráfico basado en IPs, puertos o protocolos
- Implementar listas de acceso dinámicas
- Logging de eventos de seguridad

### C) Monitoreo de Red
- Recolección de estadísticas en tiempo real
- Visualización de topología
- Alertas por congestión o fallos

### D) QoS (Quality of Service)
- Priorización de tráfico crítico
- Limitación de ancho de banda
- Clasificación automática de aplicaciones

## 6. Estructura de Entregables

### Documentación Técnica
1. **Diseño de la Arquitectura**
   - Diagramas de topología
   - Explicación de componentes
   - Justificación de decisiones

2. **Implementación**
   - Código fuente comentado
   - Instrucciones de instalación
   - Scripts de configuración

3. **Pruebas y Validación**
   - Plan de pruebas
   - Resultados obtenidos
   - Comparación con redes tradicionales

4. **Manual de Usuario**
   - Guía de uso
   - Troubleshooting
   - Ejemplos de configuración

### Código Fuente
- Controlador principal
- Aplicaciones SDN (firewall, balanceador, etc.)
- Scripts de topología
- Herramientas de monitoreo

## 7. Cronograma Sugerido (8 semanas)

**Semanas 1-2**: Estudio teórico y setup del entorno
**Semanas 3-4**: Implementación básica (aprendizaje de MACs)
**Semanas 5-6**: Funcionalidades avanzadas
**Semanas 7-8**: Pruebas, documentación y presentación

## 8. Consejos para el Éxito

### Debugging
- Usar Wireshark para analizar tráfico OpenFlow
- Logs detallados en el controlador
- Herramientas de Mininet: `dump`, `pingall`, `iperf`

### Demostración
- Preparar escenarios que muestren ventajas SDN
- Comparar rendimiento vs. redes tradicionales
- Demostrar programabilidad en vivo

### Presentación
- Enfocarse en casos de uso reales
- Mostrar código en acción
- Explicar beneficios técnicos y de negocio

## 9. Recursos Adicionales

### Documentación
- [Ryu Documentation](https://ryu.readthedocs.io/)
- [Mininet Walkthrough](http://mininet.org/walkthrough/)
- [OpenFlow Specification](https://opennetworking.org/software-defined-standards/specifications/)

### Tutoriales
- [SDN Tutorial](https://github.com/mininet/openflow-tutorial)
- [Ryu Book](https://osrg.github.io/ryu-book/en/html/)

### Herramientas de Visualización
- **Gephi**: Para graficar topologías
- **Grafana**: Para métricas en tiempo real
- **Postman**: Para APIs REST del controlador

## 10. Criterios de Evaluación Típicos

- **Funcionalidad**: ¿El sistema funciona correctamente?
- **Innovación**: ¿Qué características únicas implementaste?
- **Documentación**: ¿Está bien explicado y documentado?
- **Presentación**: ¿Puedes explicar y demostrar tu trabajo?
- **Comprensión**: ¿Entiendes los conceptos SDN subyacentes?



##  Estructura recomendada del repo

```
Proyecto-SDN/
│
├── docs/                   # Documentación
│   ├── guia_instalacion.md # Pasos para montar el entorno
│   ├── diseño_red.png      # Imagen del diagrama de red
│   ├── informe.md          # Avances o informe final
│
├── configs/                # Configuración de red
│   ├── topologia_mininet.py # Script de la topología (si es SDN)
│   ├── reglas_iptables.sh   # Ejemplo de reglas (si es Linux normal)
│
├── scripts/                # Automatización
│   ├── start_mininet.sh    # Script para correr la red
│   ├── test_connectivity.sh # Script para probar pings/iperf
│
├── resultados/             # Evidencias
│   ├── pruebas_ping.txt
│   ├── pruebas_iperf.txt
│   ├── capturas/
│       ├── ping.png
│       ├── flujo_ONOS.png
│
└── README.md               # Explicación principal del proyecto
```

---

##  Qué pueden subir

* **Código / scripts**

  * Topologías en **Mininet** (`.py`)
  * Scripts de pruebas (`.sh`)
  * Configuraciones (`.conf`)

* **Documentación**

  * Un `README.md` con:

    * Integrantes del grupo
    * Objetivo del proyecto
    * Pasos de instalación y ejecución
    * Capturas de pruebas (ping, iperf, reglas de SDN)
  * Archivos `.md` con explicaciones detalladas

* **Diagramas y evidencias**

  * Topología de la red (hecha en Draw\.io, GNS3, o a mano y escaneada).
  * Screenshots de las pruebas funcionando.
  * Logs de ejecución (`ping`, `iperf`, etc.).

* **Informe**

  * Pueden hacer el informe en Word o PDF, pero mejor en **Markdown (`.md`)** para que quede dentro del repo.

---

## Consejo para la nota

El profe va a valorar mucho si el repo tiene:

1. **README bien explicado** (que cualquiera pueda seguir y montar la red).
2. **Scripts que corran sin errores** (ejemplo: `bash start_mininet.sh`).
3. **Resultados guardados como evidencia** (logs, capturas, etc.).

---


