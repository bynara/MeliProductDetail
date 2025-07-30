#!/usr/bin/env python3
"""
Setup script for Frontend tests
Installs dependencies and verifies test environment
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        "requests",
        "pydantic",
        "pytest",
        "pytest-mock"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    return missing_packages

def setup_test_environment():
    """Set up the test environment"""
    print("=" * 60)
    print("FRONTEND TEST ENVIRONMENT SETUP")
    print("=" * 60)
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"\nInstalling missing packages: {', '.join(missing)}")
        for package in missing:
            if install_package(package):
                print(f"✅ Installed {package}")
            else:
                print(f"❌ Failed to install {package}")
    
    print("\n" + "=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print("To run tests:")
    print("  python run_working_tests.py    # Run working tests")
    print("  python run_tests.py           # Run all tests (some may fail)")
    print("  python -m unittest test_login_service.py -v  # Run specific test")

if __name__ == '__main__':
    setup_test_environment()
