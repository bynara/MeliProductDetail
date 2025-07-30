@echo off
REM MeliProductDetail - Windows Simple Runner
REM Ejecuta el proyecto sin emojis Unicode para evitar problemas de encoding

echo ===============================================
echo MELIPRODUCTDETAIL - SIMPLE RUNNER (WINDOWS)
echo ===============================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Ejecutar el script Python simple
python run_simple.py

REM Pausa al final para ver posibles errores
if errorlevel 1 (
    echo.
    echo Presiona cualquier tecla para continuar...
    pause >nul
)
