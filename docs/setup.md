# Guía de Instalación y Configuración

Esta guía te ayudará a instalar y configurar el proyecto SDN con ONOS y Mininet.

##  Requisitos del Sistema

### Hardware Recomendado
- **CPU**: 4 cores o más
- **RAM**: 8GB mínimo, 16GB recomendado
- **Almacenamiento**: 20GB de espacio libre
- **Red**: Conexión a Internet para descargar imágenes Docker

### Software Requerido
- **Docker**: 20.10 o superior
- **Docker Compose**: 1.29 o superior
- **Python**: 3.8 o superior (opcional, para scripts de automatización)
- **Git**: Para clonar el repositorio

##  Instalación Rápida (Docker)

### 1. Instalar Docker y Docker Compose

#### Ubuntu/Debian:
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Reiniciar sesión para aplicar cambios de grupo
newgrp docker
```

#### CentOS/RHEL:
```bash
# Instalar Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io

# Iniciar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Agregar usuario al grupo
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### Windows:
1. Descargar [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Ejecutar el instalador y seguir las instrucciones
3. Reiniciar el sistema
4. Docker Compose viene incluido con Docker Desktop

#### macOS:
1. Descargar [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Arrastrar a la carpeta Applications
3. Ejecutar Docker Desktop
4. Docker Compose viene incluido

### 2. Clonar y Configurar el Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/sdn-onos-mininet.git
cd sdn-onos-mininet

# Ejecutar script de setup automático
chmod +x scripts/setup.sh
./scripts/setup.sh

# Iniciar servicios
docker-compose up -d

# Verificar que los servicios están corriendo
docker-compose ps
```

### 3. Verificar la Instalación

```bash
# Verificar contenedores
docker ps

# Verificar logs de ONOS
docker-compose logs onos

# Verificar conectividad a ONOS GUI
curl -u karaf:karaf http://localhost:8181/onos/ui
```

##  Instalación Manual (Sin Docker)

### 1. Instalar Java 11

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install openjdk-11-jdk -y

# Configurar JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64' | sudo tee -a /etc/environment
source /etc/environment
```

#### CentOS/RHEL:
```bash
sudo yum install java-11-openjdk-devel -y

# Configurar JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-11-openjdk' | sudo tee -a /etc/environment
source /etc/environment
```

### 2. Instalar ONOS

```bash
# Crear directorio de instalación
sudo mkdir -p /opt
cd /opt

# Descargar ONOS
sudo wget -c https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.6.0/onos-2.6.0.tar.gz

# Extraer y renombrar
sudo tar -xzf onos-2.6.0.tar.gz
sudo mv onos-2.6.0 onos

# Configurar permisos
sudo chown -R $USER:$USER /opt/onos

# Iniciar ONOS
/opt/onos/bin/onos-service start
```

### 3. Instalar Mininet

#### Opción A: Desde repositorios (Ubuntu)
```bash
sudo apt update
sudo apt install mininet -y
```

#### Opción B: Desde código fuente
```bash
git clone https://github.com/mininet/mininet
cd mininet
git checkout -b mininet-2.3.0 2.3.0
cd util
sudo ./install.sh -a
```

### 4. Configurar Python Dependencies

```bash
# Instalar pip si no está disponible
sudo apt install python3-pip -y

# Instalar dependencias del proyecto
pip3 install --user requests pytest pyyaml python-dotenv

# O usar el archivo requirements.txt si existe
pip3 install --user -r requirements.txt
```

## ⚙️ Configuración Avanzada

### Variables de Entorno

Crea un archivo `.env` en el directorio raíz del proyecto:

```bash
# ONOS Configuration
ONOS_VERSION=2.6.0
ONOS_USER=karaf
ONOS_PASS=karaf
ONOS_HOST=localhost
ONOS_PORT=8181

# Project Configuration
PROJECT_NAME=sdn-onos-mininet
DEBUG=false

# Network Configuration
CONTROLLER_IP=127.0.0.1
OPENFLOW_PORT=6653
```

### Configuración de Red ONOS

Edita `configs/onos/network-cfg.json`:

```json
{
  "devices": {},
  "hosts": {},
  "links": {},
  "ports": {},
  "apps": {
    "org.onosproject.fwd": {
      "packetOutOnly": false,
      "packetOutOfppTable": false,
      "flowTimeout": 10,
      "ipv6Forwarding": false,
      "matchDstMacOnly": false,
      "matchVlanId": false,
      "matchIpv4Address": true,
      "matchIpv4Dscp": false,
      "matchIpv6Address": true,
      "matchIpv6FlowLabel": false,
      "matchTcpUdpPorts": false,
      "matchIcmpFields": false
    },
    "org.onosproject.acl": {
      "allowIpv6": false
    }
  }
}
```

### Configuración de Docker Compose para Producción

Para uso en producción, modifica `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  onos:
    image: onosproject/onos:2.6.0
    container_name: sdn-onos-prod
    restart: always
    ports:
      - "8181:8181"
      - "8101:8101"
      - "6653:6653"
    environment:
      - ONOS_APPS=drivers,openflow,fwd,acl,vpls,proxyarp
      - JAVA_OPTS=-Xmx4G -XX:+UseG1GC
    volumes:
      - onos_data_prod:/root/onos
      - ./configs/onos:/root/onos/config:ro
      - /etc/localtime:/etc/localtime:ro
    networks:
      - sdn_prod_network
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "5"

networks:
  sdn_prod_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/16

volumes:
  onos_data_prod:
    driver: local
```

##  Configuración de Seguridad

### 1. Cambiar Credenciales por Defecto

```bash
# Conectar al CLI de ONOS
docker exec -it sdn-onos /opt/onos/bin/onos-cli

# En el CLI de ONOS
onos> user-add admin admin123 Administrator
onos> user-remove karaf
onos> logout
```

### 2. Configurar HTTPS (Opcional)

```bash
# Generar certificado SSL
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configurar ONOS para usar HTTPS
# Editar /opt/onos/etc/org.ops4j.pax.web.cfg
echo "org.osgi.service.http.secure.enabled=true" >> /opt/onos/etc/org.ops4j.pax.web.cfg
echo "org.osgi.service.http.port.secure=8443" >> /opt/onos/etc/org.ops4j.pax.web.cfg
```

### 3. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 8181/tcp  # ONOS GUI
sudo ufw allow 8101/tcp  # ONOS CLI
sudo ufw allow 6653/tcp  # OpenFlow
sudo ufw enable

# iptables (RHEL/CentOS)
sudo firewall-cmd --permanent --add-port=8181/tcp
sudo firewall-cmd --permanent --add-port=8101/tcp
sudo firewall-cmd --permanent --add-port=6653/tcp
sudo firewall-cmd --reload
```

##  Verificación de la Instalación

### 1. Test de Servicios Básicos

```bash
# Ejecutar tests de conectividad
python3 tests/test_connectivity.py

# Verificar servicios con curl
curl -u karaf:karaf http://localhost:8181/onos/v1/devices

# Test manual de ping
docker exec -it sdn-mininet mn --test pingall
```

### 2. Test de Aplicaciones SDN

```bash
# Test del firewall
python3 applications/firewall/firewall.py --action create-sample
python3 applications/firewall/firewall.py --action apply
python3 tests/test_firewall.py

# Limpiar reglas de firewall
python3 applications/firewall/firewall.py --action delete
```

### 3. Test de Performance

```bash
# Test de latencia
docker exec -it sdn-mininet mn --test iperf

# Monitoring de recursos
docker stats

# Test de carga de la API
python3 tests/test_performance.py
```

##  Troubleshooting

### Problemas Comunes

#### 1. ONOS no inicia
```bash
# Verificar logs
docker-compose logs onos

# Verificar Java
docker exec -it sdn-onos java -version

# Reiniciar servicio
docker-compose restart onos
```

#### 2. Mininet no puede conectar al controlador
```bash
# Verificar conectividad de red
docker exec -it sdn-mininet ping onos

# Verificar puerto OpenFlow
docker exec -it sdn-mininet telnet onos 6653

# Verificar configuración de red Docker
docker network inspect sdn-onos-mininet_sdn_network
```

#### 3. GUI no es accesible
```bash
# Verificar puertos
netstat -tlnp | grep 8181

# Verificar firewall
sudo ufw status

# Test desde container
docker exec -it sdn-onos curl localhost:8181/onos/ui
```

#### 4. Scripts de Python fallan
```bash
# Verificar dependencias
pip3 list | grep requests

# Verificar conectividad API
curl -u karaf:karaf http://localhost:8181/onos/v1/

# Debug mode
python3 -u applications/firewall/firewall.py --action list
```

### Logs y Debugging

```bash
# Ver todos los logs
docker-compose logs -f

# Logs específicos de ONOS
docker exec -it sdn-onos tail -f /opt/onos/log/karaf.log

# Logs de Mininet
docker-compose logs mininet

# Debug de red Docker
docker network ls
docker network inspect bridge
```

### Recovery Procedures

```bash
# Reset completo del entorno
docker-compose down -v
docker system prune -f
./scripts/setup.sh
docker-compose up -d

# Backup de configuración ONOS
docker cp sdn-onos:/opt/onos/config ./backup/

# Restore de configuración
docker cp ./backup/config sdn-onos:/opt/onos/
docker-compose restart onos
```

## 📊 Monitoreo y Métricas

### 1. Monitoreo de Contenedores

```bash
# Stats en tiempo real
docker stats

# Healthcheck
docker inspect --format='{{.State.Health.Status}}' sdn-onos

# Uso de recursos
docker exec -it sdn-onos top
```

### 2. Métricas de ONOS

```bash
# API de métricas
curl -u karaf:karaf http://localhost:8181/onos/v1/metrics

# CLI metrics
docker exec -it sdn-onos /opt/onos/bin/onos-cli summary
```

### 3. Automatización del Monitoreo

Crea un script de monitoreo `scripts/monitor.sh`:

```bash
#!/bin/bash
while true; do
    echo "=== $(date) ==="
    echo "ONOS Status: $(docker inspect --format='{{.State.Health.Status}}' sdn-onos)"
    echo "Memory Usage: $(docker stats --no-stream --format 'table {{.Container}}\t{{.MemUsage}}' sdn-onos)"
    echo "API Response: $(curl -s -o /dev/null -w "%{http_code}" -u karaf:karaf http://localhost:8181/onos/v1/devices)"
    echo ""
    sleep 60
done
```

##  Siguientes Pasos

Una vez completada la instalación:

1. **Explora la GUI**: http://localhost:8181/onos/ui
2. **Ejecuta los tutoriales**: Ver `docs/usage.md`
3. **Prueba las aplicaciones**: Firewall y VPLS
4. **Personaliza topologías**: Modifica `topologies/custom_topo.py`
5. **Desarrolla aplicaciones**: Crea nuevas aplicaciones SDN

##  Referencias Adicionales

- [Documentación oficial de ONOS](https://wiki.onosproject.org/)
- [Guía de Mininet](http://mininet.org/walkthrough/)
- [OpenFlow Specification](https://opennetworking.org/sdn-definition/)
- [Docker Compose Reference](https://docs.docker.com/compose/)

##  Soporte

Si encuentras problemas:

1. Revisa la sección de [Troubleshooting](#-troubleshooting)
2. Consulta los [Issues del repositorio](https://github.com/tu-usuario/sdn-onos-mininet/issues)
3. Crea un nuevo issue con detalles del problema
