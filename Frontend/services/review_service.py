import requests
import streamlit as st
from models.review import Review
from typing import List

def get_product_reviews(product_id) -> List[Review]:
    headers = {}
    url = f"http://localhost:8000/reviews/product/{product_id}"
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        try:
            return [Review(**r) for r in resp.json()]
        except Exception as e:
            st.error(f"Error al parsear las reviews: {e}")
            return []
    return []
