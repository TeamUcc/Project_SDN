# SDN Network Management with ONOS and Mininet

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![ONOS](https://img.shields.io/badge/ONOS-2.6.0-green.svg)](https://onosproject.org/)

Un proyecto completo de Software-Defined Networking (SDN) utilizando ONOS como controlador SDN y Mininet para la emulación de redes. Este proyecto demuestra implementaciones prácticas de casos de uso comunes en SDN incluyendo firewall L2, VPLS y balanceador de carga.

##  Características

- **Containerización completa** con Docker y Docker Compose
- **Firewall Layer 2** con ACL configurable
- **Virtual Private LAN Service (VPLS)** para segmentación de red
- **Topologías personalizables** (Tree, Torus, Linear, Custom)
- **API REST** para gestión programática
- **Interface gráfica** para visualización de topología
- **Scripts de automatización** para deployment rápido
- **Testing automatizado** con pytest

##  Requisitos

- Docker 20.10+
- Docker Compose 1.29+
- Python 3.8+ (para scripts de automatización)
- Git

##  Instalación Rápida

### Opción 1: Docker (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/TeamUcc/Project_SDN.git
cd sdn-onos-mininet

# Iniciar servicios
docker-compose up -d

# Verificar que los servicios están corriendo
docker-compose ps
```

### Opción 2: Instalación Manual

```bash
# Ejecutar script de setup
chmod +x scripts/setup.sh
./scripts/setup.sh

# Iniciar ONOS
sudo /opt/onos/bin/onos-service start

# En otra terminal, crear topología
sudo python3 topologies/simple_tree.py
```

##  Casos de Uso

### 1. Firewall Layer 2
```bash
# Activar aplicaciones necesarias
docker exec -it sdn-onos-mininet_onos_1 /opt/onos/bin/onos-cli app activate org.onosproject.openflow
docker exec -it sdn-onos-mininet_onos_1 /opt/onos/bin/onos-cli app activate org.onosproject.acl

# Aplicar reglas de firewall
python3 applications/firewall/firewall.py
```

### 2. Virtual Private LAN Service (VPLS)
```bash
# Configurar VPLS
python3 applications/vpls/vpls_setup.py

# Verificar conectividad
python3 tests/test_vpls.py
```

##  Interfaces de Usuario

- **ONOS GUI**: http://localhost:8181/onos/ui (usuario: `karaf`, password: `karaf`)
- **ONOS CLI**: `docker exec -it sdn-onos-mininet_onos_1 /opt/onos/bin/onos-cli`
- **REST API**: http://localhost:8181/onos/v1/

##  Arquitectura del Proyecto

```
┌─────────────────┐    ┌─────────────────┐
│   ONOS Controller   │    │   Python Scripts   │
│   (Docker)      │◄───┤   (Host)        │
└─────────┬───────┘    └─────────────────┘
          │
          │ OpenFlow
          ▼
┌─────────────────┐
│   Mininet       │
│   (Docker)      │
│   - Switches    │
│   - Hosts       │
│   - Links       │
└─────────────────┘
```

##  Estructura del Proyecto

```
sdn-onos-mininet/
├── applications/          # Aplicaciones SDN
├── configs/              # Archivos de configuración
├── docs/                 # Documentación detallada
├── scripts/              # Scripts de automatización
├── tests/                # Pruebas automatizadas
├── topologies/           # Definiciones de topologías
├── docker-compose.yml    # Orquestación de contenedores
└── README.md            # Este archivo
```

##  Testing

```bash
# Ejecutar todas las pruebas
python3 -m pytest tests/

# Pruebas específicas
python3 tests/test_connectivity.py
python3 tests/test_firewall.py
python3 tests/test_vpls.py
```

##  Documentación

- [Guía de Instalación](docs/setup.md)
- [Manual de Usuario](docs/usage.md)
- [Solución de Problemas](docs/troubleshooting.md)
- [API Reference](docs/api.md)

##  Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

##  Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

##  Autores

- **Tu Nombre** - *Trabajo inicial* - [tu-usuario](https://github.com/tu-usuario)

##  Reconocimientos

- [ONOS Project](https://onosproject.org/) por el excelente controlador SDN
- [Mininet Team](http://mininet.org/) por la plataforma de emulación
- [OpenFlow Foundation](https://opennetworking.org/) por el protocolo OpenFlow

##  Roadmap

- [ ] Implementar balanceador de carga
- [ ] Agregar soporte para IPv6
- [ ] Integrar con Kubernetes
- [ ] Dashboard de monitoreo en tiempo real
- [ ] Soporte para múltiples controladores (clustering)