try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..schemas.seller import SellerSchema
    from ..repository import get_all, get_item_by_id
    from .review_service import generate_general_rating
    from ..core.logger import logger
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from app.schemas.seller import SellerSchema
    from app.repository import get_all, get_item_by_id
    from app.services.review_service import generate_general_rating
    from app.core.logger import logger


def list_sellers(db: dict) -> list[SellerSchema]:
    logger.info("Starting to list all sellers")
    try:
        seller_schemas = [SellerSchema.model_validate(obj) for obj in get_all(db, "sellers")]
        logger.info(f"Successfully retrieved {len(seller_schemas)} sellers")
        return seller_schemas
    except Exception as e:
        logger.error(f"Error listing sellers: {e}")
        raise

def get_seller_by_id(db: dict, seller_id: int) -> SellerSchema | None:
    logger.info(f"Getting seller by id: {seller_id}")
    try:
        seller = get_item_by_id(db, "sellers", seller_id)
        if not seller:
            logger.warning(f"Seller with id {seller_id} not found")
            raise ValueError("Seller not found")
        seller_response = SellerSchema.model_validate(seller)
        rating_info = generate_general_rating(db, "seller_id", seller_id)
        seller_response.rating_info = rating_info
        logger.info(f"Successfully retrieved seller with id: {seller_id}")
        return seller_response
    except Exception as e:
        logger.error(f"Error getting seller by id {seller_id}: {e}")
        raise