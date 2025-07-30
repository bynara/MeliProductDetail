import requests
import streamlit as st
from models.seller import Seller

def get_seller_detail(seller_id):
    headers = {}
    url = f"http://localhost:8000/sellers/{seller_id}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        try:
            return Seller(**resp.json())
        except Exception as e:
            st.error(f"Error al parsear el vendedor: {e}")
            return None
    return None
