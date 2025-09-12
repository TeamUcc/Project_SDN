#!/bin/bash
# ZeroTrust-SDN Setup Script
# Instala todas las dependencias necesarias para el proyecto

echo "🔒 Iniciando instalación de ZeroTrust-SDN..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para logging
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar si es Ubuntu
if [[ ! -f /etc/lsb-release ]]; then
    error "Este script está diseñado para Ubuntu"
    exit 1
fi

# Actualizar sistema
log "Actualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias base
log "Instalando dependencias base..."
sudo apt install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    wget \
    unzip \
    net-tools \
    tcpdump \
    wireshark \
    openssl \
    build-essential \
    openvswitch-switch \
    openvswitch-testcontroller

# Instalar Mininet
log "Instalando Mininet..."
if ! command -v mn &> /dev/null; then
    git clone https://github.com/mininet/mininet.git /tmp/mininet
    cd /tmp/mininet
    sudo ./util/install.sh -nwv
    cd -
else
    log "Mininet ya está instalado"
fi

# Crear entorno virtual Python
log "Creando entorno virtual Python..."
python3 -m venv venv
source venv/bin/activate

# Instalar paquetes Python
log "Instalando paquetes Python..."
pip install --upgrade pip
pip install \
    ryu \
    requests \
    pyyaml \
    prometheus-client \
    flask \
    netaddr \
    scapy

# Instalar Suricata
log "Instalando Suricata..."
sudo apt install -y suricata

# Configurar permisos para Wireshark (opcional)
log "Configurando permisos de red..."
sudo usermod -aG wireshark $USER

# Crear estructura de directorios
log "Creando estructura de directorios..."
mkdir -p {apps,mininet,suricata/{config,scripts,logs},security/certificates,monitoring,scripts,tests,docs/diagrams,demo/scenarios}

# Crear archivo requirements.txt
log "Creando requirements.txt..."
cat > requirements.txt << 'EOF'
ryu>=4.34
requests>=2.28.0
pyyaml>=6.0
prometheus-client>=0.15.0
flask>=2.2.0
netaddr>=0.8.0
scapy>=2.4.5
EOF

# Verificar instalaciones
log "Verificando instalaciones..."

echo "🧪 Verificando componentes:"
echo -n "  - Python3: "
if command -v python3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} $(python3 --version)"
else
    echo -e "${RED}✗${NC} No encontrado"
fi

echo -n "  - Pip: "
if command -v pip &> /dev/null; then
    echo -e "${GREEN}✓${NC} $(pip --version | cut -d' ' -f1-2)"
else
    echo -e "${RED}✗${NC} No encontrado"
fi

echo -n "  - Mininet: "
if command -v mn &> /dev/null; then
    echo -e "${GREEN}✓${NC} Instalado"
else
    echo -e "${RED}✗${NC} No encontrado"
fi

echo -n "  - Open vSwitch: "
if command -v ovs-vsctl &> /dev/null; then
    echo -e "${GREEN}✓${NC} $(ovs-vsctl --version | head -1)"
else
    echo -e "${RED}✗${NC} No encontrado"
fi

echo -n "  - Suricata: "
if command -v suricata &> /dev/null; then
    echo -e "${GREEN}✓${NC} $(suricata --version | head -1)"
else
    echo -e "${RED}✗${NC} No encontrado"
fi

echo -n "  - Ryu: "
if python3 -c "import ryu" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Instalado"
else
    echo -e "${RED}✗${NC} No encontrado"
fi

# Crear script de activación rápida
log "Creando script de activación..."
cat > activate.sh << 'EOF'
#!/bin/bash
# Script para activar el entorno de desarrollo
source venv/bin/activate
echo "🔒 Entorno ZeroTrust-SDN activado"
echo "Usa 'deactivate' para salir"
EOF
chmod +x activate.sh

echo ""
echo "🎉 Instalación completada!"
echo ""
echo "Para activar el entorno:"
echo "  source activate.sh"
echo ""
echo "Para probar Mininet:"
echo "  sudo mn --test pingall"
echo ""
echo "Para iniciar el controlador Ryu:"
echo "  ryu-manager apps/zero_trust_controller.py"
echo ""

warn "IMPORTANTE: Es recomendable reiniciar el sistema para aplicar todos los cambios de permisos"