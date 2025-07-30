#!/usr/bin/env python3
"""
MeliProductDetail - Stable Full Stack Runner
Versión mejorada con manejo robusto de errores y reinicio automático
"""

import os
import sys
import subprocess
import time
import platform
import signal
from pathlib import Path

# Configuración
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "Backend"
FRONTEND_DIR = PROJECT_ROOT / "Frontend"
VENV_DIR = PROJECT_ROOT / "mlvenv"

class ProcessManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def get_python_executable(self):
        """Obtiene el ejecutable de Python correcto"""
        if VENV_DIR.exists():
            if platform.system() == "Windows":
                return str(VENV_DIR / "Scripts" / "python.exe")
            else:
                return str(VENV_DIR / "bin" / "python")
        return sys.executable
    
    def check_backend_health(self):
        """Verifica si el backend está funcionando"""
        try:
            # Usar el mismo Python que ejecuta los procesos para hacer requests
            python_exe = self.get_python_executable()
            result = subprocess.run([
                python_exe, "-c", 
                "import requests; r = requests.get('http://localhost:8000/', timeout=3); print(r.status_code)"
            ], capture_output=True, text=True, timeout=5)
            return result.returncode == 0 and "200" in result.stdout
        except Exception:
            return False
    
    def start_backend(self):
        """Inicia el backend con manejo robusto"""
        python_exe = self.get_python_executable()
        backend_env = os.environ.copy()
        backend_env["PYTHONPATH"] = str(BACKEND_DIR)
        
        print("Iniciando Backend (FastAPI)...")
        
        try:
            self.backend_process = subprocess.Popen(
                [python_exe, "-m", "uvicorn", "app.main:app", 
                 "--host", "127.0.0.1", "--port", "8000", "--reload"],
                cwd=str(BACKEND_DIR),
                env=backend_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Esperar y verificar
            for i in range(20):  # 20 segundos max
                if self.backend_process.poll() is not None:
                    stdout, stderr = self.backend_process.communicate()
                    print("ERROR: Backend falló al iniciar:")
                    print("STDOUT:", stdout[-500:] if stdout else "Sin salida")
                    print("STDERR:", stderr[-500:] if stderr else "Sin errores")
                    return False
                
                if i > 5 and self.check_backend_health():
                    print("OK: Backend iniciado y funcionando")
                    return True
                
                time.sleep(1)
            
            print("WARN: Backend iniciado pero no responde")
            return False
            
        except Exception as e:
            print(f"ERROR: Error iniciando backend: {e}")
            return False
    
    def start_frontend(self):
        """Inicia el frontend"""
        python_exe = self.get_python_executable()
        
        print("Iniciando Frontend (Streamlit)...")
        
        try:
            self.frontend_process = subprocess.Popen(
                [python_exe, "-m", "streamlit", "run", "app.py", 
                 "--server.port=8502", "--server.headless=true"],
                cwd=str(FRONTEND_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            time.sleep(5)  # Dar tiempo a Streamlit
            
            if self.frontend_process.poll() is None:
                print("OK: Frontend iniciado")
                return True
            else:
                print("ERROR: Frontend falló al iniciar")
                return False
                
        except Exception as e:
            print(f"ERROR: Error iniciando frontend: {e}")
            return False
    
    def monitor_and_restart(self):
        """Monitorea procesos y reinicia si es necesario"""
        print("\n" + "=" * 60)
        print("APLICACION FUNCIONANDO")
        print("=" * 60)
        print("Backend:  http://localhost:8000")
        print("Frontend: http://localhost:8502")
        print("API Docs: http://localhost:8000/docs")
        print("=" * 60)
        print("Presiona Ctrl+C para detener")
        print("=" * 60)
        
        backend_restart_count = 0
        last_health_check = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # Verificar backend cada 10 segundos
                if current_time - last_health_check > 10:
                    if not self.check_backend_health():
                        print("⚠️  Backend no responde - reiniciando...")
                        self.restart_backend()
                        backend_restart_count += 1
                        
                        if backend_restart_count > 5:
                            print("❌ Demasiados reinicios del backend - deteniendo")
                            break
                    
                    last_health_check = current_time
                
                # Verificar si los procesos están vivos
                if self.backend_process and self.backend_process.poll() is not None:
                    print("⚠️  Backend se detuvo - reiniciando...")
                    self.restart_backend()
                    backend_restart_count += 1
                
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("⚠️  Frontend se detuvo - reiniciando...")
                    self.start_frontend()
                
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo aplicación...")
            self.running = False
            self.cleanup()
    
    def restart_backend(self):
        """Reinicia el backend"""
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        return self.start_backend()
    
    def cleanup(self):
        """Limpia procesos al salir"""
        print("🧹 Limpiando procesos...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend detenido")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("⚠️  Backend forzado a terminar")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend detenido")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("⚠️  Frontend forzado a terminar")
        
        print("👋 ¡Hasta luego!")

def main():
    """Función principal"""
    print("=" * 60)
    print("MELIPRODUCTDETAIL - STABLE RUNNER")
    print("=" * 60)
    print("Backend: FastAPI + JWT Authentication")
    print("Frontend: Streamlit + Product Detail UI")
    print("Auto-restart y health check incluidos")
    print("=" * 60)
    
    manager = ProcessManager()
    
    # Configurar signal handler
    def signal_handler(sig, frame):
        print("\nSeñal de interrupción recibida")
        manager.running = False
        manager.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Iniciar servicios
    if not manager.start_backend():
        print("ERROR: No se pudo iniciar el backend")
        sys.exit(1)
    
    if not manager.start_frontend():
        print("ERROR: No se pudo iniciar el frontend")
        manager.cleanup()
        sys.exit(1)
    
    # Monitorear
    manager.monitor_and_restart()

if __name__ == "__main__":
    main()
