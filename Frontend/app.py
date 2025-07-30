import streamlit as st

from services.login_service import get_token


def handle_login(username, password):
    try:
        token = get_token(username, password)
        return token
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def process_login():
    # Credenciales por defecto
    username = "testuser"
    password = "testpass"
    token = handle_login(username, password)
    if token:
        st.session_state['logged_in'] = True
        st.session_state['token'] = token
        st.session_state['show_product_detail'] = True
        show_product_detail_view()
    elif token is None:
        pass  # Error ya mostrado en handle_login
    else:
        st.error("Login failed")

def show_product_detail_view():
    from pages import product_detail
    # Puedes cambiar el ID de producto por uno válido en tu base de datos
    product_id = 1
    product_detail.show_product_detail(product_id)

def main():
    # Hacer la página más ancha usando el layout "wide"
    st.set_page_config(page_title="Product Detail MeLi", page_icon="assets/icon.png")
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'token' not in st.session_state:
        st.session_state['token'] = None

    if not st.session_state['logged_in']:
        process_login()
    elif st.session_state.get('show_product_detail', False):
        show_product_detail_view()


if __name__ == "__main__":
    main()