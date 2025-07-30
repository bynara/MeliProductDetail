#!/bin/bash
# MeliProductDetail - Linux/Mac Shell Runner
# Este script facilita la ejecución en sistemas Unix

echo "======================================================================"
echo "🚀 MELIPRODUCTDETAIL - UNIX RUNNER"
echo "======================================================================"

#!/bin/bash
# MeliProductDetail - Unix/Linux/macOS Launcher
# Ejecuta el proyecto completo en sistemas Unix-like

echo "======================================================================"
echo "🚀 MELIPRODUCTDETAIL - UNIX LAUNCHER"
echo "======================================================================"
echo "Sistema: $(uname -s) $(uname -m)"
echo ""

# Cambiar al directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Función para detectar el comando Python correcto
detect_python() {
    if command -v python3 &> /dev/null; then
        local version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
        local major=$(echo $version | cut -d. -f1)
        local minor=$(echo $version | cut -d. -f2)
        
        if [ "$major" -ge 3 ] && [ "$minor" -ge 7 ]; then
            echo "python3"
            return 0
        fi
    fi
    
    if command -v python &> /dev/null; then
        local version=$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
        local major=$(echo $version | cut -d. -f1)
        local minor=$(echo $version | cut -d. -f2)
        
        if [ "$major" -ge 3 ] && [ "$minor" -ge 7 ]; then
            echo "python"
            return 0
        fi
    fi
    
    return 1
}

# Detectar Python
if PYTHON_CMD=$(detect_python); then
    echo "✓ Python encontrado: $PYTHON_CMD"
    echo "✓ Version: $($PYTHON_CMD --version)"
else
    echo "❌ ERROR: Python 3.7+ no encontrado"
    echo ""
    echo "Instrucciones de instalación por sistema:"
    echo ""
    case "$(uname -s)" in
        Linux*)
            echo "Ubuntu/Debian:"
            echo "  sudo apt update && sudo apt install python3 python3-pip python3-venv"
            echo ""
            echo "CentOS/RHEL/Fedora:"
            echo "  sudo dnf install python3 python3-pip  # Fedora"
            echo "  sudo yum install python3 python3-pip  # CentOS/RHEL"
            echo ""
            echo "Arch Linux:"
            echo "  sudo pacman -S python python-pip"
            ;;
        Darwin*)
            echo "macOS:"
            echo "  # Usando Homebrew (recomendado):"
            echo "  brew install python3"
            echo ""
            echo "  # O usando el instalador oficial:"
            echo "  # Descargar desde https://www.python.org/downloads/"
            ;;
        *)
            echo "Sistema Unix detectado. Instala Python 3.7+ usando tu gestor de paquetes."
            ;;
    esac
    echo ""
    exit 1
fi

echo ""

# Verificar que los archivos necesarios existan
if [ ! -f "run_simple.py" ]; then
    echo "❌ ERROR: No se encuentra run_simple.py en el directorio actual"
    echo "Asegúrate de ejecutar este script desde el directorio raíz del proyecto"
    exit 1
fi

# Hacer que el script sea ejecutable si no lo es
if [ ! -x "$0" ]; then
    echo "🔧 Haciendo el script ejecutable..."
    chmod +x "$0"
fi

# Ejecutar el script principal
echo "🚀 Iniciando MeliProductDetail..."
echo "📂 Directorio: $SCRIPT_DIR"
echo ""

$PYTHON_CMD run_simple.py

# Capturar el código de salida
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Aplicación terminada correctamente"
else
    echo "❌ Error ejecutando el proyecto (código: $EXIT_CODE)"
    echo ""
    echo "Consejos para solucionar problemas:"
    echo "- Verifica que tienes permisos de escritura en el directorio"
    echo "- Asegúrate de tener conexión a internet para instalar dependencias"
    echo "- Revisa que los puertos 8000 y 8502 estén libres"
    echo ""
    echo "Para más ayuda, lee RUN.md o ejecuta: cat RUN.md"
    echo ""
    echo "Presiona Enter para continuar..."
    read
fi

exit $EXIT_CODE
