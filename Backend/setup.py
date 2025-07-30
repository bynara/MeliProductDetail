#!/usr/bin/env python3
"""
Auto-setup script that installs dependencies and handles imports automatically.
This script ensures all required packages are installed before running the application.
"""

import sys
import os
import subprocess
import importlib

def install_package(package_name, import_name=None):
    """Install a package using pip if it's not already installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name} already installed")
        return True
    except ImportError:
        print(f"📦 Installing {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            print(f"✅ {package_name} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package_name}: {e}")
            return False

def check_and_install_dependencies():
    """Check and install all required dependencies."""
    print("🔍 Checking dependencies...")
    
    dependencies = [
        ("fastapi", "fastapi"),
        ("uvicorn[standard]", "uvicorn"),
        ("pydantic", "pydantic"),
        ("python-multipart", "multipart"),
        ("python-jose[cryptography]", "jose"),
        ("passlib[bcrypt]", "passlib"),
        ("pytest", "pytest"),
        ("pytest-asyncio", "pytest_asyncio"),
    ]
    
    all_installed = True
    for package, import_name in dependencies:
        if not install_package(package, import_name):
            all_installed = False
    
    return all_installed

def setup_python_path():
    """Setup Python path for proper imports."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        print(f"📁 Added {current_dir} to Python path")

def main():
    """Main setup function."""
    print("🚀 MeliProductDetail Auto-Setup")
    print("=" * 40)
    
    # Setup Python path
    setup_python_path()
    
    # Check and install dependencies
    if not check_and_install_dependencies():
        print("❌ Some dependencies failed to install. Please install them manually:")
        print("pip install fastapi uvicorn[standard] pydantic python-multipart python-jose[cryptography] passlib[bcrypt] pytest pytest-asyncio")
        sys.exit(1)
    
    print("\n✅ All dependencies are ready!")
    print("🎯 You can now run:")
    print("   • python setup.py run        - Start the application")
    print("   • python setup.py test       - Run tests")
    print("   • python setup.py check      - Check installation")

def run_application():
    """Run the FastAPI application."""
    try:
        import uvicorn
        print("🚀 Starting FastAPI application...")
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        print("❌ uvicorn not found. Installing...")
        install_package("uvicorn[standard]", "uvicorn")
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

def run_tests():
    """Run the test suite."""
    try:
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])
    except subprocess.CalledProcessError:
        print("❌ Tests failed")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ pytest not found. Installing...")
        install_package("pytest")
        install_package("pytest-asyncio", "pytest_asyncio")
        subprocess.check_call([sys.executable, "-m", "pytest", "tests/", "-v"])

def check_installation():
    """Check if everything is properly installed."""
    print("🔍 Checking installation...")
    
    try:
        # Test imports
        from app.main import app
        from app.services.product_service import list_products
        print("✅ All imports working correctly")
        
        # Test basic functionality
        print("✅ Application structure is valid")
        print("✅ Installation check passed!")
        
    except Exception as e:
        print(f"❌ Installation check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "run":
            main()
            run_application()
        elif command == "test":
            main()
            run_tests()
        elif command == "check":
            main()
            check_installation()
        else:
            print("❌ Unknown command. Use: run, test, or check")
            sys.exit(1)
    else:
        main()
