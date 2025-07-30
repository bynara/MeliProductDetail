@echo off
REM Script para limpiar procesos que puedan estar bloqueando los puertos

echo Limpiando procesos del proyecto MeliProductDetail...
echo.

REM Matar procesos de Python que puedan estar usando los puertos
echo Buscando procesos en puerto 8000 (Backend)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
    echo Terminando proceso %%a
    taskkill /f /pid %%a 2>nul
)

echo Buscando procesos en puerto 8501 (Frontend)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8501"') do (
    echo Terminando proceso %%a
    taskkill /f /pid %%a 2>nul
)

echo Buscando procesos en puerto 8502 (Frontend alternativo)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8502"') do (
    echo Terminando proceso %%a
    taskkill /f /pid %%a 2>nul
)

echo.
echo Limpieza completada.
echo.
pause
