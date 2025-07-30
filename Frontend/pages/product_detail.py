
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


def load_product_detail_css():
    """Load product detail specific CSS styles from external file"""
    try:
        with open("assets/product_detail_styles.css", "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Could not load product detail CSS styles file.")


# Ensure the assets directory and no_image.png exist to avoid file-not-found errors
if not os.path.exists("assets"):
    os.makedirs("assets")
if not os.path.exists(NO_IMAGE_PATH):
    img = Image.new("RGB", (100, 100), color=(200, 200, 200))
    img.save(NO_IMAGE_PATH)


def open_image_from_url(img_url, timeout=3):
    try:
        resp = requests.get(img_url, timeout=timeout)
        img = Image.open(BytesIO(resp.content))
        img = img.convert("RGB")
        return img
    except Exception:
        return None


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
        st.info("No rating data available")

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
        <div style='background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%); 
                    color: #c62828; 
                    padding: 0.8rem; 
                    border-radius: 8px; 
                    border-left: 4px solid #f44336; 
                    font-weight: 600;
                    margin: 0.5rem 0;'>
            <strong>LOW STOCK:</strong> Only {product.stock} units remaining
        </div>
        """, unsafe_allow_html=True)
    elif product.stock < 20:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%); 
                    color: #ef6c00; 
                    padding: 0.8rem; 
                    border-radius: 8px; 
                    border-left: 4px solid #ff9800; 
                    font-weight: 600;
                    margin: 0.5rem 0;'>
            <strong>STOCK:</strong> {product.stock} units available
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); 
                    color: #2e7d32; 
                    padding: 0.8rem; 
                    border-radius: 8px; 
                    border-left: 4px solid #4caf50; 
                    font-weight: 600;
                    margin: 0.5rem 0;'>
            <strong>IN STOCK:</strong> {product.stock} units available
        </div>
        """, unsafe_allow_html=True)

def render_product_categories(product):
    if product.categories:
        st.markdown("""
        <div style='margin: 1rem 0;'>
            <h4 style='color: #3483fa; 
                       font-weight: 600; 
                       font-size: 1rem; 
                       margin-bottom: 0.5rem;
                       text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                CATEGORIES
            </h4>
        </div>
        """, unsafe_allow_html=True)
        for cat in product.categories:
            st.markdown(f"• {cat.name}")

def render_product_payment_methods(product):
    if product.payment_methods:
        st.markdown("""
        <div style='margin: 1rem 0;'>
            <h4 style='color: #00a650; 
                       font-weight: 600; 
                       font-size: 1rem; 
                       margin-bottom: 0.5rem;
                       text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                PAYMENT METHODS
            </h4>
        </div>
        """, unsafe_allow_html=True)
        payment_names = [pm.name for pm in product.payment_methods]
        st.markdown(f"• {', '.join(payment_names)}")
    else:
        st.markdown("""
        <div style='margin: 1rem 0;'>
            <h4 style='color: #666666; 
                       font-weight: 600; 
                       font-size: 1rem; 
                       margin-bottom: 0.5rem;
                       text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                PAYMENT METHODS
            </h4>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("Not specified")

def render_product_features(product):
    if product.features:
        st.markdown("""
        <div style='margin: 1rem 0;'>
            <h4 style='color: #3483fa; 
                       font-weight: 600; 
                       font-size: 1rem; 
                       margin-bottom: 0.5rem;
                       text-transform: uppercase;
                       letter-spacing: 0.5px;'>
                FEATURES
            </h4>
        </div>
        """, unsafe_allow_html=True)
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
    if related.images:
        img = open_image_from_url(related.images[0])
        if img:
            buf = BytesIO()
            img.thumbnail((70, 70))
            img.save(buf, format="PNG")
            img_b64 = base64.b64encode(buf.getvalue()).decode()
            return f"<img src='data:image/png;base64,{img_b64}' width='70'/>"
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

def render_single_related_product(related, col):
    with col:
        table_html = get_related_product_table_html(related)
        st.markdown(table_html, unsafe_allow_html=True)
        

def render_related_products(similar_products, vertical=False):
    """Render related products using pre-fetched similar products data"""
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h3 style='color: #2c3e50; 
                   font-weight: 700; 
                   font-size: 1.6rem; 
                   margin-bottom: 0.5rem;
                   text-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                   text-transform: uppercase;
                   letter-spacing: 1px;'>
            RELATED PRODUCTS
        </h3>
        <div style='width: 60px; 
                    height: 3px; 
                    background: linear-gradient(135deg, #3483fa 0%, #1565c0 100%); 
                    margin: 0 auto; 
                    border-radius: 2px;'>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if similar_products:
        if vertical:
            for related in similar_products:
                col = st.container()
                render_single_related_product(related, col)
                st.markdown("---")
        else:
            cols = st.columns(len(similar_products))
            for idx, related in enumerate(similar_products):
                render_single_related_product(related, cols[idx])
    else:
        st.info("No related products available.")


def render_checkout_info(product: Product):
    st.markdown('---')
    
    st.markdown("""
    <div style='color: #00a650; 
                font-weight: 600; 
                font-size: 1rem; 
                margin: 1rem 0;'>
        FREE SHIPPING AVAILABLE
    </div>
    """, unsafe_allow_html=True)
    
    if product.stock > 0:
        st.markdown("""
        <div style='color: #00a650; 
                    font-weight: 600; 
                    font-size: 1rem; 
                    margin: 1rem 0;'>
            IN STOCK
        </div>
        """, unsafe_allow_html=True)
        
        load_product_detail_css()
        
        st.number_input(
            "Quantity",
            min_value=1,
            max_value=product.stock,
            value=1,
            step=1,
            key="quantity_input"
        )
    else:
        st.markdown("""
        <div style='color: #d32f2f; 
                    font-weight: 600; 
                    font-size: 1rem; 
                    margin: 1rem 0;'>
            OUT OF STOCK
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="checkout-button">
        Buy now
    </div>
    
    <div class="cart-button">
        Add to Cart
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    **Free Returns**  
    You have 30 days from when you receive it.
    
    **Protected Purchase**  
    Get the product you expected or we'll refund your money.
    
    **Warranty**  
    1 year manufacturer warranty.
    """)
    
def render_seller_info(product: Product):
    st.markdown("---")
    st.markdown("""
    <div style='margin: 1.5rem 0;'>
        <h4 style='color: #3483fa; 
                   font-weight: 600; 
                   font-size: 1.2rem; 
                   margin-bottom: 1rem;
                   border-bottom: 1px solid #dee2e6;
                   padding-bottom: 0.5rem;
                   text-transform: uppercase;
                   letter-spacing: 0.5px;'>
            SELLER INFORMATION
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
                        color: #3483fa; 
                        margin-bottom: 0.5rem;'>
                {seller.name}
            </div>
            <div style='color: #666; 
                        font-size: 0.9rem; 
                        margin-bottom: 1rem;'>
                <strong>Location:</strong> {seller.location}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if seller.rating_info:
            st.markdown(f"""
            <div style='margin: 1rem 0;'>
                <div style='display: flex; 
                            align-items: center; 
                            gap: 0.5rem;
                            margin-bottom: 0.5rem;'>
                    <span style='color: #00a650; 
                                 font-size: 1.1rem; 
                                 font-weight: 600;'>
                        {seller.rating_info.average_rating:.1f}
                    </span>
                    <span style='color: #ffc107; 
                                 font-size: 1rem;'>
                        ★★★★★
                    </span>
                </div>
                <div style='background: #eeeeee; 
                            height: 4px; 
                            border-radius: 2px; 
                            margin: 0.5rem 0;
                            position: relative;'>
                    <div style='background: #3483fa; 
                                height: 4px; 
                                border-radius: 2px; 
                                width: {(seller.rating_info.average_rating / 5) * 100}%;'>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No seller reputation data available.")
    else:
        st.error("Seller information could not be retrieved.")

def render_reviews(product: Product):
    st.markdown("---")
    st.markdown("""
    <div style='margin: 2rem 0 1.5rem 0;'>
        <h3 style='color: #3483fa; 
                   font-weight: 700; 
                   font-size: 1.5rem; 
                   margin-bottom: 0.5rem;
                   border-bottom: 2px solid #3483fa;
                   padding-bottom: 0.5rem;
                   text-transform: uppercase;
                   letter-spacing: 0.5px;'>
            PRODUCT REVIEWS
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
                        border-left: 4px solid #3483fa;'>
                <div style='font-weight: 600; color: #2c3e50; margin-bottom: 0.5rem;'>
                    {review.buyer} - <span style='color: #ffc107;'>{review.rating} ★</span>
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
    st.markdown("""
    <div style='margin: 1rem 0;'>
        <h3 style='color: #3483fa; 
                   font-weight: 600; 
                   font-size: 1.3rem; 
                   text-transform: uppercase;
                   letter-spacing: 0.5px;'>
            DESCRIPTION
        </h3>
    </div>
    """, unsafe_allow_html=True)
    st.write(product.description or "No description available.")
                
def show_product_detail(product_id: int):
    if not product_id:
        st.warning("No product specified.")
        return

    product = get_product_detail(product_id)
    if not product:
        st.error("Product not found.")
        return

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