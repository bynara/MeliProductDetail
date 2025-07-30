#!/usr/bin/env python3
"""
Verification script to check that the application is properly configured.
"""

import sys
import os
import importlib

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print(f"❌ Python {sys.version_info.major}.{sys.version_info.minor} is not supported")
        print("💡 Please upgrade to Python 3.8 or higher")
        return False
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is compatible")
        return True

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('pydantic', 'Pydantic'),
        ('multipart', 'Python-multipart'),
        ('jose', 'Python-jose'),
        ('passlib', 'Passlib'),
        ('pytest', 'Pytest')
    ]
    
    all_good = True
    for package, display_name in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {display_name}")
        except ImportError:
            print(f"❌ {display_name} not found")
            all_good = False
    
    return all_good

def check_project_structure():
    """Check if project structure is correct."""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'app/__init__.py',
        'app/main.py',
        'app/core/security.py',
        'app/core/logger.py',
        'app/services/product_service.py',
        'app/controllers/product_controller.py',
        'app/schemas/product.py',
        'app/repository/__init__.py',
        'tests/test_product_service.py',
        'Data/products.json',
        'requirements.txt'
    ]
    
    all_good = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} not found")
            all_good = False
    
    return all_good

def check_imports():
    """Check if critical imports work."""
    print("\n🔗 Checking imports...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app.main import app
        print("✅ Main application")
        
        from app.services.product_service import list_products
        print("✅ Product service")
        
        from app.controllers.product_controller import router
        print("✅ Product controller")
        
        from app.schemas.product import ProductSchema
        print("✅ Product schema")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_quick_test():
    """Run a quick test to verify functionality."""
    print("\n🧪 Running quick test...")
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_product_service.py::TestProductService::test_product_schema_validation", 
            "-v", "--tb=short"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Quick test passed")
            return True
        else:
            print("❌ Quick test failed")
            print(result.stdout)
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main verification function."""
    print("🔍 MeliProductDetail - System Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Imports", check_imports),
        ("Quick Test", run_quick_test)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        try:
            if not check_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} check failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Your system is ready.")
        print("\n🚀 You can now run:")
        print("   • python run.py          - Start the application")
        print("   • python setup.py run    - Start with auto-setup")
        print("   • python -m pytest tests/ - Run all tests")
    else:
        print("❌ Some checks failed. Please review the issues above.")
        print("\n💡 Try running:")
        print("   • python setup.py        - Auto-install dependencies")
        print("   • pip install -r requirements.txt - Manual install")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
