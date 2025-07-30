#!/usr/bin/env python3
"""
Script de diagnóstico para MeliProductDetail
Identifica problemas comunes en la aplicación
"""

import sys
import requests
import json
from pathlib import Path

def check_backend_connection():
    """Verifica la conexión con el backend"""
    print("=== DIAGNÓSTICO BACKEND ===")
    
    try:
        # Verificar si el backend responde
        response = requests.get("http://localhost:8000", timeout=5)
        print("✅ Backend está respondiendo")
    except requests.exceptions.ConnectionError:
        print("❌ Backend no está disponible en http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False
    
    try:
        # Verificar endpoint de documentación
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Documentación API disponible")
        else:
            print(f"⚠️ Documentación API responde con código: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accediendo a documentación: {e}")
    
    return True

def check_authentication():
    """Verifica el sistema de autenticación"""
    print("\n=== DIAGNÓSTICO AUTENTICACIÓN ===")
    
    try:
        # Intentar obtener token
        response = requests.post(
            "http://localhost:8000/token",
            data={
                "username": "testuser",
                "password": "testpass"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print("✅ Autenticación funcionando correctamente")
            print(f"✅ Token obtenido: {token[:20]}...")
            return token
        else:
            print(f"❌ Error en autenticación: {response.status_code}")
            print(f"❌ Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
        return None

def check_product_endpoint(token):
    """Verifica el endpoint de productos"""
    print("\n=== DIAGNÓSTICO PRODUCTOS ===")
    
    if not token:
        print("❌ No hay token para verificar productos")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Probar producto ID 2 (usado en la app)
        response = requests.get(
            "http://localhost:8000/products/2",
            headers=headers,
            timeout=5
        )
        
        if response.status_code == 200:
            product_data = response.json()
            print("✅ Endpoint de productos funcionando")
            print(f"✅ Producto encontrado: {product_data.get('title', 'Sin título')[:50]}...")
            return True
        else:
            print(f"❌ Error obteniendo producto: {response.status_code}")
            print(f"❌ Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando productos: {e}")
        return False

def check_frontend_files():
    """Verifica que los archivos del frontend existan"""
    print("\n=== DIAGNÓSTICO ARCHIVOS FRONTEND ===")
    
    frontend_dir = Path("Frontend")
    required_files = [
        "app.py",
        "pages/product_detail.py",
        "services/product_service.py",
        "services/login_service.py",
        "models/product.py"
    ]
    
    all_good = True
    for file_path in required_files:
        full_path = frontend_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - FALTANTE")
            all_good = False
    
    return all_good

def check_streamlit_status():
    """Verifica si Streamlit está funcionando"""
    print("\n=== DIAGNÓSTICO STREAMLIT ===")
    
    try:
        response = requests.get("http://localhost:8502", timeout=5)
        if response.status_code == 200:
            print("✅ Streamlit está respondiendo")
            return True
        else:
            print(f"⚠️ Streamlit responde con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Streamlit no está disponible en http://localhost:8502")
        return False
    except Exception as e:
        print(f"❌ Error conectando a Streamlit: {e}")
        return False

def run_diagnostics():
    """Ejecuta todos los diagnósticos"""
    print("🔍 INICIANDO DIAGNÓSTICO COMPLETO\n")
    
    # Verificar archivos
    files_ok = check_frontend_files()
    
    # Verificar backend
    backend_ok = check_backend_connection()
    
    # Verificar autenticación
    token = None
    if backend_ok:
        token = check_authentication()
    
    # Verificar productos
    products_ok = False
    if token:
        products_ok = check_product_endpoint(token)
    
    # Verificar Streamlit
    streamlit_ok = check_streamlit_status()
    
    # Resumen
    print("\n" + "="*50)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("="*50)
    print(f"Archivos Frontend: {'✅' if files_ok else '❌'}")
    print(f"Backend API: {'✅' if backend_ok else '❌'}")
    print(f"Autenticación: {'✅' if token else '❌'}")
    print(f"Productos: {'✅' if products_ok else '❌'}")
    print(f"Streamlit: {'✅' if streamlit_ok else '❌'}")
    
    if all([files_ok, backend_ok, token, products_ok, streamlit_ok]):
        print("\n🎉 ¡Todo parece estar funcionando correctamente!")
        print("Si aún hay problemas, intenta:")
        print("1. Recargar la página de Streamlit (F5)")
        print("2. Reiniciar ambos servidores")
        print("3. Limpiar cache del navegador")
    else:
        print("\n⚠️ Se encontraron problemas. Recomendaciones:")
        if not backend_ok:
            print("- Reinicia el backend: cd Backend && python run.py")
        if not streamlit_ok:
            print("- Reinicia el frontend: cd Frontend && streamlit run app.py --server.port=8502")
        if not token:
            print("- Verifica las credenciales de prueba en el backend")
        if not files_ok:
            print("- Verifica que todos los archivos estén presentes")

if __name__ == "__main__":
    run_diagnostics()
