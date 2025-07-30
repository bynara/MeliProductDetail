#!/bin/bash

# MeliProductDetail - Instalador Automático para Linux
# Instala todas las dependencias del sistema y Python necesarias

set -e  # Salir si hay errores

echo "=================================================================="
echo "🐧 MELIPRODUCTDETAIL - INSTALADOR AUTOMÁTICO LINUX"
echo "=================================================================="
echo ""

# Detectar distribución Linux
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    echo "❌ No se pudo detectar la distribución Linux"
    exit 1
fi

echo "📋 Sistema detectado: $OS $VER"
echo ""

# Función para instalar en Ubuntu/Debian
install_ubuntu_debian() {
    echo "🔄 Actualizando lista de paquetes..."
    sudo apt update

    echo "📦 Instalando dependencias del sistema..."
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        python3-dev \
        build-essential \
        curl \
        wget \
        git

    echo "✅ Dependencias de Ubuntu/Debian instaladas"
}

# Función para instalar en CentOS/RHEL/Fedora
install_redhat() {
    if command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
    else
        echo "❌ No se encontró gestor de paquetes (dnf/yum)"
        exit 1
    fi

    echo "🔄 Actualizando sistema con $PKG_MANAGER..."
    sudo $PKG_MANAGER update -y

    echo "📦 Instalando dependencias del sistema..."
    sudo $PKG_MANAGER install -y \
        python3 \
        python3-pip \
        python3-devel \
        gcc \
        gcc-c++ \
        make \
        curl \
        wget \
        git

    echo "✅ Dependencias de Red Hat instaladas"
}

# Función para instalar en Arch Linux
install_arch() {
    echo "🔄 Actualizando sistema..."
    sudo pacman -Syu --noconfirm

    echo "📦 Instalando dependencias del sistema..."
    sudo pacman -S --noconfirm \
        python \
        python-pip \
        base-devel \
        curl \
        wget \
        git

    echo "✅ Dependencias de Arch Linux instaladas"
}

# Instalar según la distribución
case "$OS" in
    *Ubuntu*|*Debian*)
        install_ubuntu_debian
        ;;
    *CentOS*|*"Red Hat"*|*Fedora*|*"Rocky Linux"*|*"AlmaLinux"*)
        install_redhat
        ;;
    *"Arch Linux"*)
        install_arch
        ;;
    *)
        echo "⚠️  Distribución no reconocida: $OS"
        echo "💡 Instala manualmente: python3, python3-pip, python3-venv, build-essential"
        echo "🔄 Continuando con la instalación Python..."
        ;;
esac

echo ""
echo "🐍 Verificando instalación de Python..."

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "✅ Python3 instalado: $PYTHON_VERSION"
else
    echo "❌ Python3 no encontrado después de la instalación"
    exit 1
fi

# Verificar pip
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version | awk '{print $2}')
    echo "✅ pip3 instalado: $PIP_VERSION"
else
    echo "❌ pip3 no encontrado después de la instalación"
    exit 1
fi

echo ""
echo "🎯 Verificando proyecto MeliProductDetail..."

# Cambiar al directorio del script
cd "$(dirname "$0")"

if [ ! -f "run_simple.py" ]; then
    echo "❌ ERROR: No se encuentra run_simple.py"
    echo "💡 Asegúrate de estar en el directorio correcto del proyecto"
    exit 1
fi

echo "✅ Proyecto encontrado en: $(pwd)"
echo ""

# Preguntar si ejecutar el proyecto
echo "🚀 ¿Quieres ejecutar el proyecto ahora? (y/n)"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    echo "🎉 Iniciando MeliProductDetail..."
    echo ""
    python3 run_simple.py
else
    echo ""
    echo "✅ Instalación completada"
    echo ""
    echo "Para ejecutar el proyecto posteriormente, usa:"
    echo "  ./run_unix.sh"
    echo "  # o"
    echo "  python3 run_simple.py"
    echo ""
fi

echo ""
echo "📖 Para más información, lee: cat RUN.md"
echo "=================================================================="
