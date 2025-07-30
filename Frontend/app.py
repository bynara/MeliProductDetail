import streamlit as st

from services.login_service import get_token


def load_css():
    """Cargar estilos CSS desde archivo externo"""
    try:
        with open("assets/styles.css", "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("No se pudo cargar el archivo de estilos CSS.")


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
    
    # Cargar estilos CSS desde archivo externo
    load_css()
    
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