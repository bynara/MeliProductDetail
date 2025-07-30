try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..repository import get_all, get_item_by_id
    from ..schemas.category import CategorySchema
    from ..core.logger import logger
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from app.repository import get_all, get_item_by_id
    from app.schemas.category import CategorySchema
    from app.core.logger import logger

def list_categories(db: dict) -> list[CategorySchema]:
    logger.info("Starting to list all categories")
    try:
        categories = [CategorySchema.model_validate(obj) for obj in get_all(db, "categories")]
        logger.info(f"Successfully retrieved {len(categories)} categories")
        return categories
    except Exception as e:
        logger.error(f"Error listing categories: {e}")
        raise

def get_category_by_id(db: dict, category_id: int) -> CategorySchema:
    logger.info(f"Getting category by id: {category_id}")
    try:
        category = CategorySchema.model_validate(get_item_by_id(db, "categories", category_id))
        logger.info(f"Successfully retrieved category with id: {category_id}")
        return category
    except Exception as e:
        logger.error(f"Error getting category by id {category_id}: {e}")
        raise