#!/bin/bash

# MeliProductDetail - Linux Launcher
# Ejecuta el proyecto completo en sistemas Linux/Unix

echo "==============================================="
echo "MELIPRODUCTDETAIL - LINUX LAUNCHER"
echo "==============================================="
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Verificar si Python está disponible
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python no encontrado. Por favor instala Python 3.7+ primero."
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Arch Linux: sudo pacman -S python python-pip"
    exit 1
fi

echo "Usando Python: $PYTHON_CMD"
echo "Version: $($PYTHON_CMD --version)"
echo ""

# Ejecutar el script simple (compatible con Linux)
echo "Iniciando MeliProductDetail..."
$PYTHON_CMD run_simple.py

# Capturar el código de salida
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "Error ejecutando el proyecto (código: $EXIT_CODE)"
    echo "Presiona Enter para continuar..."
    read
fi

exit $EXIT_CODE
