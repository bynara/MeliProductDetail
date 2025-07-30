import streamlit as st

from services.login_service import get_token


def handle_login(username, password):
    try:
        token = get_token(username, password)
        return token
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


def show_product_detail_view():
    from pages import product_detail
    # You can change the product ID to a valid one in your database
    product_id = 1
    product_detail.show_product_detail(product_id)

def main():
    # Make the page wider using "wide" layout
    st.set_page_config(
        page_title="Product Detail MeLi", 
        page_icon="assets/icon.png",
        initial_sidebar_state="collapsed"
    )
    
    # Header estilo MercadoLibre
    # Convertir la imagen a base64 para incluirla en el HTML
    import base64
    try:
        with open("assets/logo_meli.webp", "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            logo_html = f'<img src="data:image/webp;base64,{img_data}" alt="MercadoLibre" style="height: 40px; max-width: 200px; object-fit: contain;">'
    except FileNotFoundError:
        logo_html = '<span style="font-family: Arial, sans-serif; font-size: 24px; font-weight: bold; color: #333;">MercadoLibre</span>'
    
    st.markdown(f"""
    <div style="background-color: #FFE600; padding: 20px; margin: -1rem -1rem 2rem -1rem; border-bottom: 1px solid #ccc; width: calc(100% + 2rem); margin-left: -1rem; box-sizing: border-box;">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: flex-start;">
            {logo_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CSS para la aplicación
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Eliminar fondos blancos que interfieren con el header */
    div[data-testid="stVerticalBlock"] > div:first-child {
        background-color: transparent !important;
    }
    div[data-testid="element-container"]:first-child {
        background-color: transparent !important;
    }
    
    /* Main application styling */
    .stApp {
        background-color: white !important;
        font-family: 'Inter', sans-serif !important;
        color: #2c3e50 !important;
    }
    
    /* Remove default Streamlit padding */
    .main .block-container {
        background-color: white !important;
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Input and selectbox styling */
    .stSelectbox > div > div {
        background-color: white !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
        transition: border-color 0.2s ease !important;
        color: #2c3e50 !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #1976d2 !important;
    }
    
    .stSelectbox label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    .stNumberInput > div > div > input {
        background-color: white !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
        color: #2c3e50 !important;
        font-weight: 500 !important;
        transition: border-color 0.2s ease !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #1976d2 !important;
        box-shadow: 0 0 0 0.2rem rgba(25, 118, 210, 0.25) !important;
    }
    
    .stNumberInput label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: #1976d2 !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(25, 118, 210, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3) !important;
        background: #1565c0 !important;
    }
    
    /* Text and markdown styling */
    .stMarkdown {
        background-color: white !important;
        color: #2c3e50 !important;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    .stMarkdown p {
        color: #495057 !important;
        line-height: 1.6 !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background-color: #1976d2 !important;
    }
    
    .stSlider > div > div > div[role="slider"] {
        background-color: #1976d2 !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 6px rgba(25, 118, 210, 0.3) !important;
    }
    
    .stSlider label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
    }
    
    /* Info boxes styling */
    .stInfo {
        background-color: #e3f2fd !important;
        border-left: 4px solid #2196f3 !important;
        border-radius: 0 8px 8px 0 !important;
        color: #2c3e50 !important;
    }
    
    .stSuccess {
        background-color: #e8f5e8 !important;
        border-left: 4px solid #4caf50 !important;
        border-radius: 0 8px 8px 0 !important;
        color: #2c3e50 !important;
    }
    
    .stWarning {
        background-color: #fff3e0 !important;
        border-left: 4px solid #ff9800 !important;
        border-radius: 0 8px 8px 0 !important;
        color: #2c3e50 !important;
    }
    
    .stError {
        background-color: #ffebee !important;
        border-left: 4px solid #f44336 !important;
        border-radius: 0 8px 8px 0 !important;
        color: #2c3e50 !important;
    }
    
    /* Ensure text visibility */
    label, span, div {
        color: #2c3e50 !important;
    }
    
    /* Link styling */
    a {
        color: #1976d2 !important;
        text-decoration: none !important;
        transition: color 0.2s ease !important;
    }
    
    a:hover {
        color: #1565c0 !important;
        text-decoration: underline !important;
    }
    
    /* Column styling */
    div[data-testid="column"] {
        background-color: white !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* Tables styling */
    table, tbody, thead, tr, td, th {
        background-color: white !important;
        border-color: #e9ecef !important;
        color: #2c3e50 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Breadcrumb navigation estilo MercadoLibre
    st.markdown("""
    <div style="
        background-color: #f5f5f5;
        padding: 12px 20px;
        margin: 0 -1rem 1.5rem -1rem;
        font-size: 13px;
        color: #666;
        border-bottom: 1px solid #e6e6e6;
    ">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center;">
            <a href="#" style="color: #3B82F6; text-decoration: none; font-weight: 500;">Inicio</a>
            <span style="margin: 0 8px; color: #ccc; font-weight: 300;">></span>
            <a href="#" style="color: #3B82F6; text-decoration: none; font-weight: 500;">Tecnología</a>
            <span style="margin: 0 8px; color: #ccc; font-weight: 300;">></span>
            <a href="#" style="color: #3B82F6; text-decoration: none; font-weight: 500;">Celulares y Teléfonos</a>
            <span style="margin: 0 8px; color: #ccc; font-weight: 300;">></span>
            <span style="color: #666; font-weight: 400;">Celulares y Smartphones</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    show_product_detail_view()


if __name__ == "__main__":
    main()