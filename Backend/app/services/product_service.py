try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..schemas.product import ProductSchema
    from ..schemas.category import CategorySchema
    from ..schemas.payment_method import PaymentMethodSchema
    from ..repository import get_all, get_item_by_id
    from .review_service import generate_general_rating
    from ..core.logger import logger
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from app.schemas.product import ProductSchema
    from app.schemas.category import CategorySchema
    from app.schemas.payment_method import PaymentMethodSchema
    from app.repository import get_all, get_item_by_id
    from app.services.review_service import generate_general_rating
    from app.core.logger import logger

def enrich_product(obj: dict, db: dict) -> dict:
    logger.debug(f"Enriching product with id: {obj.get('id')}")
    try:
        category_ids = set(obj.get("category_ids", []))
        payment_methods_ids = set(obj.get("payment_methods_ids", []))

        # Enrich categories
        obj["categories"] = [
            CategorySchema.model_validate(cat)
            for cat in db.get("categories", [])
            if cat.get("id") in category_ids
        ]
        # Enrich payment methods
        obj["payment_methods"] = [
            PaymentMethodSchema.model_validate(pm)
            for pm in db.get("payment_methods", [])
            if pm.get("id") in payment_methods_ids
        ]

        # Enrich ratings and reviews using generate_general_rating
        general_rating = generate_general_rating(db, "product_id", obj["id"])
        obj["rating_info"] = general_rating

        logger.debug(f"Successfully enriched product with id: {obj.get('id')}")
        return obj
    except Exception as e:
        logger.error(f"Error enriching product with id {obj.get('id')}: {e}")
        raise RuntimeError(f"Error enriching product: {e}")

def list_products(db: dict) -> list[ProductSchema]:
    logger.info("Starting to list all products")
    try:
        products = [
            ProductSchema.model_validate(enrich_product(obj, db))
            for obj in get_all(db, "products")
        ]
        logger.info(f"Successfully retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Error listing products: {e}")
        raise RuntimeError(f"Error listing products: {e}")

def get_product_by_id(db: dict, product_id: int) -> ProductSchema:
    logger.info(f"Getting product by id: {product_id}")
    try:
        obj = get_item_by_id(db, "products", product_id)
        product = ProductSchema.model_validate(enrich_product(obj, db))
        logger.info(f"Successfully retrieved product with id: {product_id}")
        return product
    except Exception as e:
        logger.error(f"Error getting product by id {product_id}: {e}")
        raise RuntimeError(f"Error getting product by id {product_id}: {e}")

def get_similar_products(db: dict, product_id: int, limit: int = 5) -> list[ProductSchema]:
    logger.info(f"Getting similar products for product id: {product_id}")
    obj = get_item_by_id(db, "products", product_id)
    product = ProductSchema.model_validate(obj)
    target_categories = set(getattr(product, "category_ids", []))
    if not target_categories:
        logger.info(f"No categories found for product id: {product_id}. Returning empty list.")
        return []
    all_products = [ProductSchema.model_validate(obj) for obj in get_all(db, "products")]
    similarities = []
    for p in all_products:
        if p.id == product_id:
            continue
        if(p.category_ids is None):
            continue
        shared = len(target_categories.intersection(set(getattr(p, "category_ids", []))))
        if shared > 0:
            similarities.append((shared, p))
    similarities.sort(key=lambda x: (-x[0], x[1].id))
    top_products = [p for _, p in similarities[:limit]]
    logger.info(f"Found {len(top_products)} similar products for product id: {product_id}")
    return top_products