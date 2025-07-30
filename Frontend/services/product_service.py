import requests
import streamlit as st
from models.product import Product
from typing import Optional, List


HEADERS = {}

def get_product_detail(product_id: str) -> Optional[Product]:
    url = f"http://localhost:8000/products/{product_id}"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        try:
            data = resp.json()
            # Asegurarse de que los campos opcionales estén presentes
            if 'categories' not in data:
                data['categories'] = None
            if 'payment_methods' not in data:
                data['payment_methods'] = None
            if 'features' not in data:
                data['features'] = None
            if 'rating_info' not in data:
                data['rating_info'] = None
            return Product(**data)
        except Exception as e:
            st.error(f"Error al parsear el producto: {e}")
            return None
    return None

# Servicio para obtener productos similares
def get_similar_products(product_id: str) -> List[Product]:
    url = f"http://localhost:8000/products/{product_id}/similar"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 200:
        try:
            return [Product(**item) for item in resp.json()]
        except Exception as e:
            st.error(f"Error al parsear productos similares: {e}")
            return []
    return []
