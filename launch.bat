@echo off
title MeliProductDetail - Launcher
echo.
echo ===============================================
echo    MeliProductDetail - Automatic Launcher
echo ===============================================
echo.

REM Execute PowerShell script bypassing execution policy
echo Starting services...
echo.
powershell -ExecutionPolicy Bypass -File "start.ps1"

echo.
echo Press any key to exit...
pause >nul
