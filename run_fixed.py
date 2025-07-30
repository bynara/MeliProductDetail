#!/usr/bin/env python3
"""
MeliProductDetail - Fixed Runner
Versión simplificada que resuelve el problema de cuelgue del backend
"""

import os
import sys
import subprocess
import time
import platform
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "Backend"
FRONTEND_DIR = PROJECT_ROOT / "Frontend"
VENV_DIR = PROJECT_ROOT / "mlvenv"

def get_python_executable():
    """Obtiene el ejecutable de Python correcto"""
    if VENV_DIR.exists():
        if platform.system() == "Windows":
            return str(VENV_DIR / "Scripts" / "python.exe")
        else:
            return str(VENV_DIR / "bin" / "python")
    return sys.executable

def install_dependencies():
    """Instala dependencias básicas"""
    python_exe = get_python_executable()
    
    deps = [
        "fastapi", "uvicorn[standard]", "python-jose[cryptography]",
        "python-multipart", "passlib[bcrypt]", "pydantic>=2.0.0",
        "streamlit", "requests", "Pillow"
    ]
    
    print("Instalando dependencias...")
    for dep in deps:
        try:
            subprocess.run([python_exe, "-m", "pip", "install", dep], 
                         check=True, capture_output=True)
            print(f"OK: {dep}")
        except subprocess.CalledProcessError:
            print(f"WARN: Fallo {dep}")

def start_backend_simple():
    """Inicia el backend de forma simple"""
    python_exe = get_python_executable()
    
    print("Iniciando Backend...")
    print("URL: http://localhost:8000")  # Cambiar puerto
    
    # Usar uvicorn directamente para evitar problemas con run.py
    try:
        backend_process = subprocess.Popen(
            [python_exe, "-m", "uvicorn", "app.main:app", 
             "--host", "127.0.0.1", "--port", "8000", "--reload"],  # Puerto 8000
            cwd=str(BACKEND_DIR),
            env=dict(os.environ, PYTHONPATH=str(BACKEND_DIR))
        )
        
        time.sleep(8)  # Dar tiempo al backend
        
        if backend_process.poll() is None:
            print("OK: Backend iniciado")
            return backend_process
        else:
            print("ERROR: Backend falló")
            return None
            
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def start_frontend_simple():
    """Inicia el frontend de forma simple"""
    python_exe = get_python_executable()
    
    print("Iniciando Frontend...")
    print("URL: http://localhost:8502")
    
    try:
        frontend_process = subprocess.Popen(
            [python_exe, "-m", "streamlit", "run", "app.py", "--server.port=8502"],
            cwd=str(FRONTEND_DIR)
        )
        
        time.sleep(5)
        
        if frontend_process.poll() is None:
            print("OK: Frontend iniciado")
            return frontend_process
        else:
            print("ERROR: Frontend falló")
            return None
            
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    """Función principal simplificada"""
    print("=" * 50)
    print("MELIPRODUCTDETAIL - FIXED RUNNER")
    print("=" * 50)
    
    # Verificar estructura
    if not BACKEND_DIR.exists() or not FRONTEND_DIR.exists():
        print("ERROR: Estructura de proyecto inválida")
        return
    
    # Instalar dependencias
    install_dependencies()
    
    # Iniciar servicios
    backend = start_backend_simple()
    if not backend:
        print("ERROR: No se pudo iniciar el backend")
        return
    
    frontend = start_frontend_simple()
    if not frontend:
        print("ERROR: No se pudo iniciar el frontend")
        if backend:
            backend.terminate()
        return
    
    print("\n" + "=" * 50)
    print("APLICACION FUNCIONANDO")
    print("=" * 50)
    print("Backend:  http://localhost:8000")  # Puerto actualizado
    print("Frontend: http://localhost:8502")
    print("Docs:     http://localhost:8000/docs")  # Puerto actualizado
    print("=" * 50)
    print("Presiona Ctrl+C para detener")
    
    try:
        while True:
            # Monitoreo simple
            if backend.poll() is not None:
                print("WARN: Backend se detuvo")
                break
            if frontend.poll() is not None:
                print("WARN: Frontend se detuvo")
                break
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nDeteniendo...")
        
        if backend:
            backend.terminate()
        if frontend:
            frontend.terminate()
        
        print("Detenido.")

if __name__ == "__main__":
    main()
