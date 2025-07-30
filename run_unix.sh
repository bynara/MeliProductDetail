#!/bin/bash
# MeliProductDetail - Linux/Mac Shell Runner
# Este script facilita la ejecución en sistemas Unix

echo "======================================================================"
echo "🚀 MELIPRODUCTDETAIL - UNIX RUNNER"
echo "======================================================================"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Error: Python no está instalado"
    echo "💡 Instala Python 3.7+ desde tu gestor de paquetes"
    exit 1
fi

# Determinar comando de Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "🚀 Iniciando aplicación completa con $PYTHON_CMD..."
$PYTHON_CMD run_fullstack.py
