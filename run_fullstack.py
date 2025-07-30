#!/usr/bin/env python3
"""
MeliProductDetail - Full Stack Runner
Ejecuta tanto el frontend como el backend simultáneamente
Instala automáticamente todas las dependencias necesarias
"""

import os
import sys
import subprocess
import threading
import time
import signal
import platform
from pathlib import Path

# Configurar encoding para Windows
if platform.system() == "Windows":
    import locale
    import codecs
    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout.detach())
    sys.stderr = codecs.getwriter(locale.getpreferredencoding())(sys.stderr.detach())

# Configuración
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "Backend"
FRONTEND_DIR = PROJECT_ROOT / "Frontend"
VENV_DIR = PROJECT_ROOT / "mlvenv"

class Colors:
    """Colores para output en terminal"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message, color=Colors.WHITE):
    """Imprime mensaje con color"""
    print(f"{color}{message}{Colors.END}")

def print_banner():
    """Imprime banner de inicio"""
    print_colored("=" * 70, Colors.CYAN)
    print_colored("🚀 MELIPRODUCTDETAIL - FULL STACK RUNNER", Colors.BOLD + Colors.BLUE)
    print_colored("=" * 70, Colors.CYAN)
    print_colored("📦 Backend: FastAPI + JWT Authentication", Colors.GREEN)
    print_colored("🎨 Frontend: Streamlit + Product Detail UI", Colors.GREEN)
    print_colored("🔧 Auto-instalación de dependencias incluida", Colors.YELLOW)
    print_colored("=" * 70, Colors.CYAN)

def check_python_version():
    """Verifica la versión de Python"""
    print_colored("🐍 Verificando versión de Python...", Colors.BLUE)
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_colored("❌ Error: Se requiere Python 3.7 o superior", Colors.RED)
        print_colored(f"   Versión actual: {version.major}.{version.minor}.{version.micro}", Colors.RED)
        sys.exit(1)
    print_colored(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado", Colors.GREEN)

def get_python_executable():
    """Obtiene el ejecutable de Python correcto"""
    if VENV_DIR.exists():
        if platform.system() == "Windows":
            return str(VENV_DIR / "Scripts" / "python.exe")
        else:
            return str(VENV_DIR / "bin" / "python")
    return sys.executable

def check_and_create_venv():
    """Verifica y crea el entorno virtual si es necesario"""
    if not VENV_DIR.exists():
        print_colored("📦 Creando entorno virtual...", Colors.YELLOW)
        try:
            subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
            print_colored("✅ Entorno virtual creado exitosamente", Colors.GREEN)
        except subprocess.CalledProcessError as e:
            print_colored(f"❌ Error creando entorno virtual: {e}", Colors.RED)
            sys.exit(1)
    else:
        print_colored("✅ Entorno virtual encontrado", Colors.GREEN)

def install_package(python_exe, package, description=""):
    """Instala un paquete usando pip"""
    try:
        print_colored(f"📦 Instalando {package} {description}...", Colors.YELLOW)
        subprocess.run(
            [python_exe, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            check=True
        )
        print_colored(f"✅ {package} instalado exitosamente", Colors.GREEN)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Error instalando {package}: {e}", Colors.RED)
        return False

def check_and_install_dependencies():
    """Verifica e instala todas las dependencias necesarias"""
    python_exe = get_python_executable()
    
    print_colored("🔍 Verificando dependencias...", Colors.BLUE)
    
    # Dependencias del backend
    backend_deps = [
        ("fastapi", "framework web"),
        ("uvicorn[standard]", "servidor ASGI"),
        ("python-jose[cryptography]", "JWT tokens"),
        ("python-multipart", "formularios"),
        ("passlib[bcrypt]", "hashing passwords"),
        ("pydantic>=2.0.0", "validación datos"),
        ("pytest", "testing framework")
    ]
    
    # Dependencias del frontend
    frontend_deps = [
        ("streamlit", "framework UI"),
        ("requests", "HTTP cliente"),
        ("Pillow", "procesamiento imágenes"),
        ("streamlit-carousel", "componente carousel")
    ]
    
    all_deps = backend_deps + frontend_deps
    
    print_colored(f"📋 Instalando {len(all_deps)} dependencias...", Colors.BLUE)
    
    failed_packages = []
    for package, description in all_deps:
        if not install_package(python_exe, package, f"({description})"):
            failed_packages.append(package)
    
    if failed_packages:
        print_colored(f"⚠️ Algunos paquetes fallaron: {', '.join(failed_packages)}", Colors.YELLOW)
        print_colored("   El proyecto puede funcionar parcialmente", Colors.YELLOW)
    else:
        print_colored("✅ Todas las dependencias instaladas correctamente", Colors.GREEN)

def start_backend():
    """Inicia el servidor backend"""
    python_exe = get_python_executable()
    backend_env = os.environ.copy()
    backend_env["PYTHONPATH"] = str(BACKEND_DIR)
    
    print_colored("🔧 Iniciando Backend (FastAPI)...", Colors.PURPLE)
    print_colored("   📍 URL: http://localhost:8000", Colors.CYAN)
    print_colored("   📖 Docs: http://localhost:8000/docs", Colors.CYAN)
    
    try:
        # Usar el script run.py del backend que maneja las dependencias
        backend_process = subprocess.Popen(
            [python_exe, "run.py"],
            cwd=str(BACKEND_DIR),
            env=backend_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Leer output del backend en tiempo real
        for line in iter(backend_process.stdout.readline, ''):
            if line.strip():
                print_colored(f"[BACKEND] {line.strip()}", Colors.PURPLE)
            if "Application startup complete" in line or "Uvicorn running on" in line:
                print_colored("✅ Backend iniciado exitosamente", Colors.GREEN)
                break
        
        return backend_process
    except Exception as e:
        print_colored(f"❌ Error iniciando backend: {e}", Colors.RED)
        return None

def start_frontend():
    """Inicia el servidor frontend"""
    python_exe = get_python_executable()
    
    print_colored("🎨 Iniciando Frontend (Streamlit)...", Colors.BLUE)
    print_colored("   📍 URL: http://localhost:8501", Colors.CYAN)
    
    try:
        frontend_process = subprocess.Popen(
            [python_exe, "-m", "streamlit", "run", "app.py", "--server.port=8501"],
            cwd=str(FRONTEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Esperar a que Streamlit inicie
        for line in iter(frontend_process.stdout.readline, ''):
            if line.strip():
                print_colored(f"[FRONTEND] {line.strip()}", Colors.BLUE)
            if "You can now view your Streamlit app" in line or "Network URL:" in line:
                print_colored("✅ Frontend iniciado exitosamente", Colors.GREEN)
                break
        
        return frontend_process
    except Exception as e:
        print_colored(f"❌ Error iniciando frontend: {e}", Colors.RED)
        return None

def terminate_process(process, name):
    """Termina un proceso de manera segura"""
    if process:
        process.terminate()
        try:
            process.wait(timeout=5)
            print_colored(f"✅ {name} detenido", Colors.GREEN)
        except subprocess.TimeoutExpired:
            process.kill()
            print_colored(f"� {name} forzado a terminar", Colors.YELLOW)

def check_processes_alive(backend_process, frontend_process):
    """Verifica si los procesos siguen vivos"""
    if backend_process and backend_process.poll() is not None:
        print_colored("⚠️ Backend se detuvo inesperadamente", Colors.YELLOW)
        return False
    if frontend_process and frontend_process.poll() is not None:
        print_colored("⚠️ Frontend se detuvo inesperadamente", Colors.YELLOW)
        return False
    return True

def monitor_processes(backend_process, frontend_process):
    """Monitorea los procesos y maneja la terminación"""
    print_colored("\n" + "=" * 70, Colors.CYAN)
    print_colored("🎉 APLICACIÓN FUNCIONANDO", Colors.BOLD + Colors.GREEN)
    print_colored("=" * 70, Colors.CYAN)
    print_colored("🔧 Backend:  http://localhost:8000", Colors.PURPLE)
    print_colored("🎨 Frontend: http://localhost:8501", Colors.BLUE)
    print_colored("📖 API Docs: http://localhost:8000/docs", Colors.CYAN)
    print_colored("=" * 70, Colors.CYAN)
    print_colored("� Presiona Ctrl+C para detener ambos servidores", Colors.YELLOW)
    print_colored("=" * 70, Colors.CYAN)
    
    try:
        while True:
            if not check_processes_alive(backend_process, frontend_process):
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print_colored("\n🛑 Deteniendo servidores...", Colors.YELLOW)
        terminate_process(backend_process, "Backend")
        terminate_process(frontend_process, "Frontend")
        print_colored("👋 ¡Hasta luego!", Colors.CYAN)

def verify_directories():
    """Verifica que existan los directorios necesarios"""
    if not BACKEND_DIR.exists():
        print_colored(f"❌ Error: No se encuentra el directorio Backend en {BACKEND_DIR}", Colors.RED)
        return False
    
    if not FRONTEND_DIR.exists():
        print_colored(f"❌ Error: No se encuentra el directorio Frontend en {FRONTEND_DIR}", Colors.RED)
        return False
    
    if not (BACKEND_DIR / "app" / "main.py").exists() and not (BACKEND_DIR / "run.py").exists():
        print_colored("❌ Error: No se encuentra main.py o run.py en Backend", Colors.RED)
        return False
    
    if not (FRONTEND_DIR / "app.py").exists():
        print_colored("❌ Error: No se encuentra app.py en Frontend", Colors.RED)
        return False
    
    return True

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones iniciales
    check_python_version()
    
    if not verify_directories():
        print_colored("❌ Estructura de proyecto inválida", Colors.RED)
        sys.exit(1)
    
    # Configurar entorno virtual y dependencias
    check_and_create_venv()
    check_and_install_dependencies()
    
    print_colored("\n🚀 Iniciando aplicación completa...", Colors.BOLD + Colors.BLUE)
    
    # Iniciar backend
    backend_process = start_backend()
    if not backend_process:
        print_colored("❌ No se pudo iniciar el backend", Colors.RED)
        sys.exit(1)
    
    # Esperar un poco para que el backend esté listo
    time.sleep(3)
    
    # Iniciar frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print_colored("❌ No se pudo iniciar el frontend", Colors.RED)
        if backend_process:
            backend_process.terminate()
        sys.exit(1)
    
    # Monitorear ambos procesos
    monitor_processes(backend_process, frontend_process)

if __name__ == "__main__":
    main()
