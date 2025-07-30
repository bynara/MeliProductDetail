@echo off
REM MeliProductDetail - Windows Optimized Runner
REM Ejecuta el proyecto usando el script optimizado para Windows

echo ===============================================
echo MELIPRODUCTDETAIL - OPTIMIZED RUNNER (WINDOWS)
echo ===============================================
echo Backend: FastAPI + JWT Authentication (Puerto 8000)
echo Frontend: Streamlit + Product Detail UI (Puerto 8502)
echo Optimizado para Windows - Sin problemas Unicode/Performance
echo ===============================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Verificar que existe el entorno virtual
if not exist "mlvenv" (
    echo Creando entorno virtual...
    python -m venv mlvenv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        echo Verifica que Python este instalado correctamente
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo Activando entorno virtual...
call mlvenv\Scripts\activate.bat

REM Ejecutar el script optimizado para Windows
echo Ejecutando aplicacion optimizada...
echo.
echo ======================================
echo USANDO SCRIPT OPTIMIZADO PARA WINDOWS
echo - Sin problemas Unicode
echo - Puerto 8000 (evita bloqueos)
echo - Configuracion estable
echo ======================================
echo.

python run_fixed.py

REM Pausa al final para ver posibles errores
if errorlevel 1 (
    echo.
    echo ERROR: La aplicacion termino con errores
    echo.
    echo SOLUCION: Revisa WINDOWS.md para guia detallada
    echo O ejecuta: python run_fixed.py desde CMD
    echo.
    echo Presiona cualquier tecla para continuar...
    pause >nul
) else (
    echo.
    echo La aplicacion se ejecuto correctamente.
    echo Presiona cualquier tecla para continuar...
    pause >nul
)
