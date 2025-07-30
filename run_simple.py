#!/usr/bin/env python3
"""
MeliProductDetail - Full Stack Runner (Windows Compatible)
Ejecuta tanto el frontend como el backend simultáneamente
Instala automáticamente todas las dependencias necesarias
"""

import os
import sys
import subprocess
import time
import platform
import requests
from pathlib import Path

# Configuración
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "Backend"
FRONTEND_DIR = PROJECT_ROOT / "Frontend"
VENV_DIR = PROJECT_ROOT / "mlvenv"

def print_banner():
    """Imprime banner de inicio"""
    print("=" * 70)
    print("MELIPRODUCTDETAIL - FULL STACK RUNNER")
    print("=" * 70)
    print("Backend: FastAPI + JWT Authentication")
    print("Frontend: Streamlit + Product Detail UI")
    print("Auto-instalacion de dependencias incluida")
    print("=" * 70)

def check_python_version():
    """Verifica la versión de Python"""
    print("Verificando version de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"ERROR: Se requiere Python 3.7 o superior")
        print(f"Version actual: {version.major}.{version.minor}.{version.micro}")
        sys.exit(1)
    print(f"OK: Python {version.major}.{version.minor}.{version.micro} detectado")

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
        print("Creando entorno virtual...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
            print("OK: Entorno virtual creado exitosamente")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Error creando entorno virtual: {e}")
            sys.exit(1)
    else:
        print("OK: Entorno virtual encontrado")

def install_package(python_exe, package, description=""):
    """Instala un paquete usando pip"""
    try:
        print(f"Instalando {package} {description}...")
        subprocess.run(
            [python_exe, "-m", "pip", "install", package],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"OK: {package} instalado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Error instalando {package}: {e}")
        return False

def check_and_install_dependencies():
    """Verifica e instala todas las dependencias necesarias"""
    python_exe = get_python_executable()
    
    print("Verificando dependencias...")
    
    # Dependencias del backend
    backend_deps = [
        ("fastapi", "(framework web)"),
        ("uvicorn[standard]", "(servidor ASGI)"),
        ("python-jose[cryptography]", "(JWT tokens)"),
        ("PyJWT>=2.10.0", "(JWT tokens adicional)"),
        ("python-multipart", "(formularios)"),
        ("passlib[bcrypt]", "(hashing passwords)"),
        ("pydantic>=2.0.0", "(validacion datos)"),
        ("requests>=2.31.0", "(HTTP cliente)"),
        ("pytest", "(testing framework)")
    ]
    
    # Dependencias del frontend
    frontend_deps = [
        ("streamlit", "(framework UI)"),
        ("requests", "(HTTP cliente)"),
        ("Pillow", "(procesamiento imagenes)"),
        ("streamlit-carousel", "(componente carousel)")
    ]
    
    all_deps = backend_deps + frontend_deps
    
    print(f"Instalando {len(all_deps)} dependencias...")
    
    failed_packages = []
    for package, description in all_deps:
        if not install_package(python_exe, package, description):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"WARN: Algunos paquetes fallaron: {', '.join(failed_packages)}")
        print("El proyecto puede funcionar parcialmente")
    else:
        print("OK: Todas las dependencias instaladas correctamente")

def check_backend_health():
    """Verifica si el backend está funcionando correctamente"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def wait_for_backend_ready(max_wait=30):
    """Espera hasta que el backend esté listo para recibir requests"""
    print("Verificando que el backend esté listo...")
    
    for i in range(max_wait):
        if check_backend_health():
            print("OK: Backend está respondiendo correctamente")
            return True
        
        if i % 5 == 0 and i > 0:
            print(f"Esperando backend... ({i}/{max_wait}s)")
        
        time.sleep(1)
    
    print("ERROR: Backend no responde después del timeout")
    return False

def start_backend():
    """Inicia el servidor backend con mejor manejo de errores"""
    python_exe = get_python_executable()
    backend_env = os.environ.copy()
    backend_env["PYTHONPATH"] = str(BACKEND_DIR)
    
    print("Iniciando Backend (FastAPI)...")
    print("URL: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    
    try:
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
        
        # Esperar y verificar que el backend inicie correctamente
        print("Esperando que el backend inicie...")
        startup_timeout = 15  # Aumentar timeout
        
        for i in range(startup_timeout):
            if backend_process.poll() is not None:
                # El proceso terminó, obtener la salida de error
                stdout, stderr = backend_process.communicate()
                print("ERROR: Backend terminó inesperadamente")
                print("STDOUT:", stdout[:1000] if stdout else "No output")
                print("STDERR:", stderr[:1000] if stderr else "No errors")
                return None
            
            time.sleep(1)
            if i % 3 == 0:  # Mostrar progreso cada 3 segundos
                print(f"Esperando backend... ({i+1}/{startup_timeout}s)")
        
        if backend_process.poll() is None:
            print("OK: Backend iniciado exitosamente")
            return backend_process
        else:
            print("ERROR: Backend fallo al iniciar después del timeout")
            return None
        
    except Exception as e:
        print(f"ERROR: Error iniciando backend: {e}")
        return None

def start_frontend():
    """Inicia el servidor frontend"""
    python_exe = get_python_executable()
    
    print("Iniciando Frontend (Streamlit)...")
    print("URL: http://localhost:8502")
    
    try:
        frontend_process = subprocess.Popen(
            [python_exe, "-m", "streamlit", "run", "app.py", "--server.port=8502"],
            cwd=str(FRONTEND_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Esperar a que Streamlit inicie
        time.sleep(5)
        
        if frontend_process.poll() is None:
            print("OK: Frontend iniciado exitosamente")
            return frontend_process
        else:
            print("ERROR: Frontend fallo al iniciar")
            return None
        
    except Exception as e:
        print(f"ERROR: Error iniciando frontend: {e}")
        return None

def restart_backend():
    """Reinicia el backend si se cuelga"""
    print("🔄 Intentando reiniciar el backend...")
    backend_process = start_backend()
    if backend_process and wait_for_backend_ready():
        print("✅ Backend reiniciado exitosamente")
        return backend_process
    else:
        print("❌ No se pudo reiniciar el backend")
        return None

def monitor_processes(backend_process, frontend_process):
    """Monitorea los procesos y maneja la terminación"""
    print("\n" + "=" * 70)
    print("APLICACION FUNCIONANDO")
    print("=" * 70)
    print("Backend:  http://localhost:8000")
    print("Frontend: http://localhost:8502")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 70)
    print("Presiona Ctrl+C para detener ambos servidores")
    print("=" * 70)
    
    try:
        check_count = 0
        while True:
            check_count += 1
            
            # Verificar backend
            if backend_process and backend_process.poll() is not None:
                print("WARN: Backend se detuvo inesperadamente")
                try:
                    stdout, stderr = backend_process.communicate(timeout=1)
                    if stdout:
                        print("Backend STDOUT:", stdout[-500:])  # Últimas 500 chars
                    if stderr:
                        print("Backend STDERR:", stderr[-500:])
                except:
                    pass
                break
            
            # Verificar frontend
            if frontend_process and frontend_process.poll() is not None:
                print("WARN: Frontend se detuvo inesperadamente")
                try:
                    stdout, stderr = frontend_process.communicate(timeout=1)
                    if stdout:
                        print("Frontend STDOUT:", stdout[-500:])
                    if stderr:
                        print("Frontend STDERR:", stderr[-500:])
                except:
                    pass
                break
            
            # Mostrar estado cada 30 segundos
            if check_count % 30 == 0:
                print(f"INFO: Aplicación funcionando correctamente ({check_count}s)")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo servidores...")
        terminate_processes(backend_process, frontend_process)

def terminate_processes(backend_process, frontend_process):
    """Termina los procesos de manera segura"""
    # Terminar backend
    if backend_process:
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
            print("OK: Backend detenido")
        except subprocess.TimeoutExpired:
            backend_process.kill()
            print("WARN: Backend forzado a terminar")
        except Exception as e:
            print(f"ERROR: Problema terminando backend: {e}")
    
    # Terminar frontend
    if frontend_process:
        try:
            frontend_process.terminate()
            frontend_process.wait(timeout=5)
            print("OK: Frontend detenido")
        except subprocess.TimeoutExpired:
            frontend_process.kill()
            print("WARN: Frontend forzado a terminar")
        except Exception as e:
            print(f"ERROR: Problema terminando frontend: {e}")
    
    print("Hasta luego!")

def verify_directories():
    """Verifica que existan los directorios necesarios"""
    if not BACKEND_DIR.exists():
        print(f"ERROR: No se encuentra el directorio Backend en {BACKEND_DIR}")
        return False
    
    if not FRONTEND_DIR.exists():
        print(f"ERROR: No se encuentra el directorio Frontend en {FRONTEND_DIR}")
        return False
    
    if not (BACKEND_DIR / "app" / "main.py").exists() and not (BACKEND_DIR / "run.py").exists():
        print("ERROR: No se encuentra main.py o run.py en Backend")
        return False
    
    if not (FRONTEND_DIR / "app.py").exists():
        print("ERROR: No se encuentra app.py en Frontend")
        return False
    
    return True

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones iniciales
    check_python_version()
    
    if not verify_directories():
        print("ERROR: Estructura de proyecto invalida")
        sys.exit(1)
    
    # Configurar entorno virtual y dependencias
    check_and_create_venv()
    check_and_install_dependencies()
    
    print("\nIniciando aplicacion completa...")
    
    # Iniciar backend
    backend_process = start_backend()
    if not backend_process:
        print("ERROR: No se pudo iniciar el backend")
        sys.exit(1)
    
    # Verificar que el backend esté realmente funcionando
    if not wait_for_backend_ready():
        print("ERROR: Backend no está respondiendo")
        if backend_process:
            backend_process.terminate()
        sys.exit(1)
    
    # Iniciar frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("ERROR: No se pudo iniciar el frontend")
        if backend_process:
            backend_process.terminate()
        sys.exit(1)
    
    # Monitorear ambos procesos
    monitor_processes(backend_process, frontend_process)

if __name__ == "__main__":
    main()
