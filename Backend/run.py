#!/usr/bin/env python3
"""
Enhanced script to run the FastAPI application with automatic dependency management.
This handles import paths correctly and installs missing dependencies automatically.
"""

import sys
import os
import subprocess
import importlib

def install_missing_package(package_name, import_name=None):
    """Install a missing package automatically."""
    if import_name is None:
        import_name = package_name
    
    print(f"📦 Missing dependency: {import_name}")
    print(f"🔄 Installing {package_name}...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package_name}")
        return False

def ensure_dependencies():
    """Ensure all required dependencies are available."""
    required_packages = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn[standard]',
        'pydantic': 'pydantic',
        'multipart': 'python-multipart',
        'jose': 'python-jose[cryptography]',
        'passlib': 'passlib[bcrypt]'
    }
    
    missing_packages = []
    
    for import_name, package_name in required_packages.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_packages.append((import_name, package_name))
    
    if missing_packages:
        print("🔍 Checking dependencies...")
        for import_name, package_name in missing_packages:
            if not install_missing_package(package_name, import_name):
                print(f"❌ Please install manually: pip install {package_name}")
                return False
        
        print("✅ All dependencies installed!")
    
    return True

def setup_python_path():
    """Setup Python path for proper imports."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)

def main():
    """Main function to run the application."""
    setup_python_path()
    
    if not ensure_dependencies():
        print("❌ Failed to install required dependencies")
        sys.exit(1)
    
    try:
        import uvicorn
        print("Starting FastAPI application...")
        print("Server will be available at: http://localhost:8000")
        print("API documentation at: http://localhost:8000/docs")
        print("Auto-reload enabled for development")
        print("Press CTRL+C to stop")
        
        # Use import string for proper reload support
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
        
    except ImportError as e:
        print(f"Failed to import required modules: {e}")
        print("Try running: python setup.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
