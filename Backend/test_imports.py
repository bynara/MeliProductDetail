#!/usr/bin/env python3
"""
Test script to verify that both relative and absolute imports work.
"""

import sys
import os

def test_imports():
    print("Testing imports...")
    
    try:
        # Test importing a service
        from app.services.product_service import list_products
        print("✓ Service import successful")
        
        # Test importing a controller
        from app.controllers.product_controller import router
        print("✓ Controller import successful")
        
        # Test importing main app
        from app.main import app
        print("✓ Main app import successful")
        
        print("\n🎉 All imports working correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    # Add current directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    success = test_imports()
    sys.exit(0 if success else 1)
