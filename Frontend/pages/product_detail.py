
import base64
import os
import tempfile
from io import BytesIO

import requests
import streamlit as st
from PIL import Image
from streamlit_carousel import carousel

from models.product import Product
from services.product_service import get_product_detail, get_similar_products
from services.review_service import get_product_reviews
from services.seller_service import get_seller_detail

NO_IMAGE_PATH = "assets/no_image.png"

# Ensure the assets directory and no_image.png exist to avoid file-not-found errors
if not os.path.exists("assets"):
    os.makedirs("assets")
if not os.path.exists(NO_IMAGE_PATH):
    # Create a simple placeholder image if it doesn't exist
    img = Image.new("RGB", (100, 100), color=(200, 200, 200))
    img.save(NO_IMAGE_PATH)


# Utilidad para abrir imágenes desde una URL usando Pillow
def open_image_from_url(img_url, timeout=3):
    try:
        resp = requests.get(img_url, timeout=timeout)
        img = Image.open(BytesIO(resp.content))
        img = img.convert("RGB")
        return img
    except Exception:
        return None

# Guarda la imagen Pillow en un archivo temporal y retorna la ruta
def save_temp_image(img, prefix="carousel_img_"):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"{prefix}{next(tempfile._get_candidate_names())}.jpg")
    img.save(temp_path, format="JPEG")
    return temp_path




def process_and_save_image(img_url, target_width=250, target_height=400):
    img = open_image_from_url(img_url)
    if not img:
        return NO_IMAGE_PATH
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height
    # Crop the image to the target aspect ratio (center crop)
    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))
    img = img.resize((target_width, target_height), Image.LANCZOS)
    return save_temp_image(img)

def get_carousel_images(product):
    images = []
    if product.images:
        for idx, img_url in enumerate(product.images):
            img_path = process_and_save_image(img_url)
            images.append({"img": img_path, "title": f"{idx + 1}", "text": "..."})
    return images

def render_product_images(product):
    inner_col1, inner_col2 = st.columns([5, 4])
    images = get_carousel_images(product)
    with inner_col1:
        if images:
            carousel(items=images, width=250, container_height=400)
        else:
            st.info("No images available.")
    return inner_col2
    


def render_product_title(product):
    st.markdown(f"#### {product.title}")

def render_product_rating(product):
    if product.rating_info:
        avg = product.rating_info.average_rating
        reviews = product.rating_info.reviews_count
        stars = int(round(avg))
        star_html =f"<span style='color:gray; font-size:1.3em;'>{avg:.1f}</span> "
        star_html += "".join(["<span style='color:gold; font-size:1.2em;'>★</span>" for _ in range(stars)])
        star_html += "".join(["<span style='color:#ccc; font-size:1.2em;'>☆</span>" for _ in range(5 - stars)])
        star_html += f" <span style='color:#555;'>({reviews})</span>"
        st.markdown(star_html, unsafe_allow_html=True)
    else:
        st.info("No general rating data available.")

def render_product_price_and_stock(product):
    st.markdown(f"<span style='font-size:1.5em; font-weight:500;'>${product.price}</span>", unsafe_allow_html=True)
    if product.stock < 10:
        st.markdown(f"<span style='color:red'>Stock: {product.stock}</span>", unsafe_allow_html=True)
    elif product.stock < 20:
        st.markdown(f"<span style='color:orange'>Stock: {product.stock}</span>", unsafe_allow_html=True)
    else:
        st.write(f"Stock: {product.stock}")

def render_product_categories(product):
    if product.categories:
        st.write("Categories:")
        for cat in product.categories:
            st.write(f"- {cat.name}")

def render_product_payment_methods(product):
    st.write(f"Payment Methods: {', '.join([pm.name for pm in product.payment_methods] if product.payment_methods else [])}")

def render_product_features(product):
    if product.features:
        st.write("Features:")
        selected_features = {}
        for k, v in product.features.items():
            options = v if isinstance(v, list) else [v]
            selected = st.selectbox(f"Select {k}", options, key=f"feature_{k}")
            selected_features[k] = selected

def render_product_info(product, inner_col2):
    with inner_col2:
        render_product_title(product)
        render_product_rating(product)
        render_product_price_and_stock(product)
        render_product_features(product)
        render_product_categories(product)
        render_product_payment_methods(product)


def get_related_product_image_html(related):
    # Devuelve el HTML de la imagen (base64) para el producto relacionado
    if related.images:
        img = open_image_from_url(related.images[0])
        if img:
            buf = BytesIO()
            img.thumbnail((70, 70))
            img.save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            return f"<img src='data:image/png;base64,{img_b64}' width='70'/>"
    # Si no hay imagen válida, usa la de respaldo
    try:
        with open(NO_IMAGE_PATH, "rb") as f:
            img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        return f"<img src='data:image/png;base64,{img_b64}' width='70'/>"
    except Exception:
        return "<span style='color:red'>No image</span>"

def get_related_product_table_html(related, item_width=100, item_height=220):
    img_html = get_related_product_image_html(related)
    title = related.title
    if len(title) > 18:
        title = title[:15] + "..."
    return f"""
            <table style='width:{item_width}px; height:{item_height}px; text-align:center; border-collapse:collapse; background:transparent; margin:auto;'>
                <tr>
                    <td style='height:110px; vertical-align:middle; border:none; background:transparent; padding:0;'>
                        {img_html}
                    </td>
                </tr>
                <tr>
                    <td style='min-height:3.5em; height:3.5em; border:none; background:transparent;'><b>{title}</b></td>
                </tr>
                <tr>
                    <td style='font-size:1.1em; color:#1976d2; border:none; height:2.2em; background:transparent;'><b>${related.price}</b></td>
                </tr>
            </table>
        """

def render_single_related_product(related, col, vertical=False):
    with col:
        table_html = get_related_product_table_html(related)
        st.markdown(table_html, unsafe_allow_html=True)
        st.button("View", key=f"view_{'V' if vertical else 'H'}_{related.id}", use_container_width=True)

def render_related_products(product: Product, vertical=False):
    st.markdown("---")
    st.markdown("<h3 style='text-align:center;'>Related Products</h3>", unsafe_allow_html=True)
    similar_products = get_similar_products(product.id)
    if similar_products:
        if vertical:
            for related in similar_products:
                col = st.container()
                render_single_related_product(related, col, vertical=True)
                st.markdown("---")
        else:
            cols = st.columns(len(similar_products))
            for idx, related in enumerate(similar_products):
                render_single_related_product(related, cols[idx])
    else:
        st.info("No related products available.")


def render_checkout_info(product: Product):
    st.markdown('---')
    st.write("Free shipping available")
    if product.stock > 0:
        st.write("In Stock")
        st.number_input(
            "Quantity",
            min_value=1,
            max_value=product.stock,
            value=1,
            step=1,
            key="quantity_input"
        )
    else:
        st.write("Out of Stock")
    st.markdown(
        """
        <style>
        .checkout-btn button {
            background-color: #1976d2 !important;
            color: white !important;
            font-weight: bold;
            width: 100%;
            border-radius: 6px;
            margin-bottom: 1em;
            border: 2px solid transparent;
            transition: border-color 0.2s;
        }
        .checkout-btn button:hover {
            border: 2px solid #90caf9 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.button("Checkout", key="checkout_btn", help="Proceed to checkout", use_container_width=True)
    st.markdown("""
    <div style="margin-top:1em; font-size:0.98em; color:#444;">
        <p><span style='color:#00bfa5; font-weight:bold;'>Devolución gratis</span>. Tienes 30 días desde<br>
        que lo recibes.</p>
        <p><span style='color:#1976d2; font-weight:bold;'>Compra Protegida</span>, recibe el producto<br>
        que esperabas o te devolvemos tu<br>
        dinero.</p>
        <p>1 año de garantía de fábrica.</p>
    </div>
    """, unsafe_allow_html=True)
    
def render_seller_info(product: Product):
    st.markdown("---")
    seller = get_seller_detail(product.seller_id)
    if seller:
        st.markdown(
            f"<span style='color:#1976d2; font-size:1.25em; font-weight:bold;'>{seller.name}</span>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<span style='color:#607d8b; font-size:0.95em;'>Location: {seller.location}</span>",
            unsafe_allow_html=True
        )
        if seller.rating_info:
            st.slider(
                "Rating",
                min_value=0.0,
                max_value=5.0,
                value=float(seller.rating_info.average_rating),
                step=0.1,
                disabled=True,
                help=f"Based on {seller.rating_info.ratings_count} ratings"
            )
        else:
            st.info("No seller reputation data available.")
    else:
        st.error("Seller information could not be retrieved.")

def render_reviews(product: Product):
    st.markdown("---")
    st.subheader("Product reviews")
    reviews = get_product_reviews(product.id)
    if reviews:
        for review in reviews:
            st.markdown(f"**{review.buyer}** - {review.rating}⭐")
            st.write(review.review or "No review text provided.")
            st.markdown("---")
    else:
        st.info("No reviews available for this product.")

def render_product_description(product):
    st.markdown("---")
    st.markdown("### Description")
    st.write(product.description or "No description available.")
                
def show_product_detail(product_id: int):
    if not product_id:
        st.warning("No product specified.")
        return

    product = get_product_detail(product_id)
    if not product:
        st.error("Product not found.")
        return

    col1, col2 = st.columns([6, 2])
    with col1:
        inner_col2 = render_product_images(product)
        render_product_info(product, inner_col2)
        render_related_products(product)
        render_product_description(product)
        render_reviews(product)
    with col2:
        render_checkout_info(product)
        render_seller_info(product)
        render_related_products(product, vertical=True)