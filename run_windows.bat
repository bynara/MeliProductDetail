@echo off
REM MeliProductDetail - Windows Batch Runner
REM Este script facilita la ejecución en Windows

echo ======================================================================
echo 🚀 MELIPRODUCTDETAIL - WINDOWS RUNNER
echo ======================================================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en el PATH
    echo 💡 Instala Python desde https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Ejecutar el script principal
echo 🚀 Iniciando aplicación completa...
python run_fullstack.py

pause
