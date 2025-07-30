
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


# Utility to open images from a URL using Pillow
def open_image_from_url(img_url, timeout=3):
    try:
        resp = requests.get(img_url, timeout=timeout)
        img = Image.open(BytesIO(resp.content))
        img = img.convert("RGB")
        return img
    except Exception:
        return None

# Save the Pillow image to a temporary file and return the path
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
    st.markdown(f"""
    <div style='margin-bottom: 1.5rem;'>
        <h2 style='color: #2c3e50; 
                   font-weight: 700; 
                   font-size: 1.8rem; 
                   line-height: 1.3; 
                   margin-bottom: 0.5rem;
                   text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);'>
            {product.title}
        </h2>
    </div>
    """, unsafe_allow_html=True)

def render_product_rating(product):
    if product.rating_info:
        avg = product.rating_info.average_rating
        reviews = product.rating_info.reviews_count
        stars = int(round(avg))
        
        # Create visual rating display
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.markdown(f"""
            <div style='text-align: center;'>
                <span style='font-size: 2rem; font-weight: 700; color: #1976d2;'>
                    {avg:.1f}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            star_display = "★" * stars + "☆" * (5 - stars)
            st.markdown(f"""
            <div style='text-align: center; font-size: 1.8rem; color: #ffc107;'>
                {star_display}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='text-align: center; font-size: 0.9rem; color: #666;'>
                ({reviews})
            </div>
            """, unsafe_allow_html=True)
            
    else:
        st.info("📊 No rating data available")

def render_product_price_and_stock(product):
    st.markdown(f"""
    <div style='padding: 1rem 0; margin: 1rem 0;'>
        <span style='font-size: 2.2rem; 
                     font-weight: 700; 
                     color: #1976d2;'>
            ${product.price}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    if product.stock < 10:
        st.markdown(f"""
        <div style='background-color: #ffebee; 
                    color: #c62828; 
                    padding: 0.8rem; 
                    border-radius: 8px; 
                    border-left: 4px solid #f44336; 
                    font-weight: 600;
                    margin: 0.5rem 0;'>
            ⚠️ Low Stock: {product.stock} units remaining
        </div>
        """, unsafe_allow_html=True)
    elif product.stock < 20:
        st.markdown(f"""
        <div style='background-color: #fff3e0; 
                    color: #ef6c00; 
                    padding: 0.8rem; 
                    border-radius: 8px; 
                    border-left: 4px solid #ff9800; 
                    font-weight: 600;
                    margin: 0.5rem 0;'>
            📦 Stock: {product.stock} units available
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background-color: #e8f5e8; 
                    color: #2e7d32; 
                    padding: 0.8rem; 
                    border-radius: 8px; 
                    border-left: 4px solid #4caf50; 
                    font-weight: 600;
                    margin: 0.5rem 0;'>
            ✅ In Stock: {product.stock} units available
        </div>
        """, unsafe_allow_html=True)

def render_product_categories(product):
    if product.categories:
        st.markdown("**📂 Categories:**")
        for cat in product.categories:
            st.markdown(f"• {cat.name}")

def render_product_payment_methods(product):
    if product.payment_methods:
        st.markdown("**💳 Payment Methods:**")
        payment_names = [pm.name for pm in product.payment_methods]
        st.markdown(f"• {', '.join(payment_names)}")
    else:
        st.markdown("**💳 Payment Methods:** Not specified")

def render_product_features(product):
    if product.features:
        st.markdown("**⚙️ Features:**")
        selected_features = {}
        for k, v in product.features.items():
            options = v if isinstance(v, list) else [v]
            selected = st.selectbox(
                f"Select {k}", 
                options, 
                key=f"feature_{k}",
                help=f"Choose your preferred {k.lower()}"
            )
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
    # Returns the HTML of the image (base64) for the related product
    if related.images:
        img = open_image_from_url(related.images[0])
        if img:
            buf = BytesIO()
            img.thumbnail((70, 70))
            img.save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            return f"<img src='data:image/png;base64,{img_b64}' width='70'/>"
    # If there's no valid image, use the fallback
    try:
        with open(NO_IMAGE_PATH, "rb") as f:
            img_bytes = f.read()
        img_b64 = base64.b64encode(img_bytes).decode()
        return f"<img src='data:image/png;base64,{img_b64}' width='70'/>"
    except Exception:
        return "<span style='color:red'>No image</span>"

def get_related_product_table_html(related, item_width=120, item_height=280):
    img_html = get_related_product_image_html(related)
    title = related.title
    if len(title) > 25:
        title = title[:22] + "..."
    return f"""
        <div style='width: {item_width}px; 
                    height: {item_height}px; 
                    background: white; 
                    border-radius: 8px; 
                    border: 1px solid #dee2e6; 
                    padding: 1rem; 
                    text-align: center; 
                    margin: auto;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                    transition: box-shadow 0.3s ease;'>
            <div style='height: 90px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        margin-bottom: 1rem;'>
                {img_html}
            </div>
            <div style='height: auto; 
                        min-height: 4rem;
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        margin-bottom: 1rem;
                        text-align: center;'>
                <div style='color: #2c3e50; 
                            font-size: 0.85rem; 
                            line-height: 1.4; 
                            font-weight: 600;
                            word-wrap: break-word;
                            hyphens: auto;'>
                    {title}
                </div>
            </div>
            <div style='height: auto; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center;
                        padding-top: 0.5rem;
                        border-top: 1px solid #e9ecef;'>
                <strong style='font-size: 1.1rem; 
                              color: #1976d2; 
                              font-weight: 700;'>
                    ${related.price}
                </strong>
            </div>
        </div>
    """

def render_single_related_product(related, col, vertical=False):
    with col:
        table_html = get_related_product_table_html(related)
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Botón View estilizado más pequeño
        button_id = f"view_{'V' if vertical else 'H'}_{related.id}"
        st.markdown(f"""
        <style>
        .small-view-button-{button_id} {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            color: #495057;
            padding: 0.4rem 0.8rem;
            border: 1px solid #dee2e6;
            border-radius: 4px;
            font-size: 0.85rem;
            font-weight: 500;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            width: 100%;
            margin-top: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 32px;
        }}
        .small-view-button-{button_id}:hover {{
            background: linear-gradient(135deg, #e9ecef 0%, #dee2e6 100%);
            color: #343a40;
            border-color: #adb5bd;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .small-view-button-{button_id}:active {{
            transform: translateY(0px);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }}
        </style>
        
        <div class="small-view-button-{button_id}">
            View
        </div>
        """, unsafe_allow_html=True)

def render_related_products(similar_products, vertical=False):
    """Render related products using pre-fetched similar products data"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h3 style='color: #2c3e50; 
                   font-weight: 700; 
                   font-size: 1.6rem; 
                   margin-bottom: 0.5rem;
                   text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);'>
            🛍️ Related Products
        </h3>
        <div style='width: 60px; 
                    height: 3px; 
                    background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%); 
                    margin: 0 auto; 
                    border-radius: 2px;'>
        </div>
    </div>
    """, unsafe_allow_html=True)
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
    
    # Información de envío
    st.markdown("🚚 **Free shipping available**")
    
    # Estado del stock
    if product.stock > 0:
        st.markdown("✅ **In Stock**")
        
        # CSS para mejorar el number_input
        st.markdown("""
        <style>
        /* Resetear todos los estilos del number input */
        div[data-testid="stNumberInput"] input,
        .stNumberInput input,
        .stNumberInput > div > div > input,
        .stNumberInput > div > div > div > input {
            background-color: #ffffff !important;
            border: 2px solid #3483fa !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            color: #000000 !important;
            text-align: center !important;
            height: auto !important;
            min-height: 42px !important;
            box-shadow: inset 0 1px 3px rgba(0,0,0,0.1) !important;
        }
        
        div[data-testid="stNumberInput"] input:focus,
        .stNumberInput input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #1976d2 !important;
            box-shadow: 0 0 0 3px rgba(25, 118, 210, 0.3) !important;
            outline: none !important;
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        
        div[data-testid="stNumberInput"] label,
        .stNumberInput label {
            font-weight: 700 !important;
            color: #2c3e50 !important;
            font-size: 1.1rem !important;
            margin-bottom: 0.8rem !important;
        }
        
        /* Forzar visibilidad del texto */
        div[data-testid="stNumberInput"] input::selection {
            background-color: #3483fa !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.number_input(
            "Quantity",
            min_value=1,
            max_value=product.stock,
            value=1,
            step=1,
            key="quantity_input"
        )
    else:
        st.markdown("❌ **Out of Stock**")
    
    # Botón de checkout estilizado
    st.markdown("""
    <style>
    .checkout-button {
        background: linear-gradient(135deg, #3483fa 0%, #2968c8 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 6px;
        font-size: 1rem;
        font-weight: 600;
        text-align: center;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(52, 131, 250, 0.25);
        transition: all 0.2s ease;
        width: 100%;
        margin: 1rem 0;
        letter-spacing: 0.5px;
        min-height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .checkout-button:hover {
        background: linear-gradient(135deg, #2968c8 0%, #1f5bb8 100%);
        box-shadow: 0 4px 12px rgba(52, 131, 250, 0.35);
        transform: translateY(-1px);
    }
    .checkout-button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 6px rgba(52, 131, 250, 0.3);
    }
    
    .cart-button {
        background: linear-gradient(135deg, #5ba4f5 0%, #4a91e2 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 6px;
        font-size: 1rem;
        font-weight: 600;
        text-align: center;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(91, 164, 245, 0.25);
        transition: all 0.2s ease;
        width: 100%;
        margin: 0.5rem 0;
        letter-spacing: 0.5px;
        min-height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .cart-button:hover {
        background: linear-gradient(135deg, #4a91e2 0%, #3a7bc8 100%);
        box-shadow: 0 4px 12px rgba(91, 164, 245, 0.35);
        transform: translateY(-1px);
    }
    .cart-button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 6px rgba(91, 164, 245, 0.3);
    }
    </style>
    
    <div class="checkout-button">
        Buy now
    </div>
    
    <div class="cart-button">
        Add to Cart
    </div>
    """, unsafe_allow_html=True)
    
    # Información de garantías
    st.markdown("---")
    st.markdown("**🛡️ Purchase Protection**")
    
    st.markdown("""
    **🚚 Free Returns**  
    You have 30 days from when you receive it.
    
    **🛡️ Protected Purchase**  
    Get the product you expected or we'll refund your money.
    
    **⭐ Warranty**  
    1 year manufacturer warranty.
    """)
    
def render_seller_info(product: Product):
    st.markdown("---")
    st.markdown("""
    <div style='margin: 1.5rem 0;'>
        <h4 style='color: #2c3e50; 
                   font-weight: 600; 
                   font-size: 1.2rem; 
                   margin-bottom: 1rem;
                   border-bottom: 1px solid #dee2e6;
                   padding-bottom: 0.5rem;'>
            🏪 Seller Information
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    seller = get_seller_detail(product.seller_id)
    if seller:
        st.markdown(f"""
        <div style='background: #f8f9fa; 
                    border-radius: 8px; 
                    padding: 1rem; 
                    margin: 1rem 0;
                    border: 1px solid #dee2e6;'>
            <div style='font-size: 1.1rem; 
                        font-weight: 700; 
                        color: #1976d2; 
                        margin-bottom: 0.5rem;'>
                {seller.name}
            </div>
            <div style='color: #6c757d; 
                        font-size: 0.9rem; 
                        margin-bottom: 1rem;'>
                📍 Location: {seller.location}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if seller.rating_info:
            # CSS para mejorar el slider
            st.markdown("""
            <style>
            .stSlider > div > div > div > div {
                background-color: #3483fa !important;
            }
            .stSlider > div > div > div {
                background-color: #e9ecef !important;
            }
            .stSlider label {
                font-weight: 600 !important;
                color: #2c3e50 !important;
                font-size: 1rem !important;
            }
            .stSlider > div > div > div > div > div {
                background-color: #3483fa !important;
                border: 2px solid white !important;
                box-shadow: 0 2px 8px rgba(52, 131, 250, 0.3) !important;
            }
            .stSlider p {
                font-weight: 600 !important;
                color: #1976d2 !important;
                font-size: 1.1rem !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.slider(
                "Seller Rating",
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
    st.markdown("""
    <div style='margin: 2rem 0 1.5rem 0;'>
        <h3 style='color: #2c3e50; 
                   font-weight: 700; 
                   font-size: 1.5rem; 
                   margin-bottom: 0.5rem;
                   border-bottom: 2px solid #1976d2;
                   padding-bottom: 0.5rem;'>
            📝 Product Reviews
        </h3>
    </div>
    """, unsafe_allow_html=True)
    reviews = get_product_reviews(product.id)
    if reviews:
        for review in reviews:
            st.markdown(f"""
            <div style='background: #f8f9fa; 
                        border-radius: 8px; 
                        padding: 1rem; 
                        margin: 1rem 0;
                        border-left: 4px solid #1976d2;'>
                <div style='font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem;'>
                    {review.buyer} - {review.rating}⭐
                </div>
                <div style='color: #495057; line-height: 1.5;'>
                    {review.review or "No review text provided."}
                </div>
            </div>
            """, unsafe_allow_html=True)
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

    # Fetch similar products only once
    similar_products = get_similar_products(product.id)

    col1, col2 = st.columns([6, 2])
    with col1:
        inner_col2 = render_product_images(product)
        render_product_info(product, inner_col2)
        render_related_products(similar_products)
        render_product_description(product)
        render_reviews(product)
    with col2:
        render_checkout_info(product)
        render_seller_info(product)
        render_related_products(similar_products, vertical=True)