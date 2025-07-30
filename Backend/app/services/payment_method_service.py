try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..repository import get_all, get_item_by_id
    from ..schemas.payment_method import PaymentMethodSchema
    from ..core.logger import logger
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from app.repository import get_all, get_item_by_id
    from app.schemas.payment_method import PaymentMethodSchema
    from app.core.logger import logger

def list_payment_methods(db: dict) -> list[PaymentMethodSchema]:
    logger.info("Starting to list all payment methods")
    try:
        payment_methods = [PaymentMethodSchema.model_validate(obj) for obj in get_all(db, "payment_methods")]
        logger.info(f"Successfully retrieved {len(payment_methods)} payment methods")
        return payment_methods
    except Exception as e:
        logger.error(f"Error listing payment methods: {e}")
        raise

def get_payment_method_by_id(db: dict, payment_method_id: int) -> PaymentMethodSchema:
    logger.info(f"Getting payment method by id: {payment_method_id}")
    try:
        payment_method = PaymentMethodSchema.model_validate(get_item_by_id(db, "payment_methods", payment_method_id))
        logger.info(f"Successfully retrieved payment method with id: {payment_method_id}")
        return payment_method
    except Exception as e:
        logger.error(f"Error getting payment method by id {payment_method_id}: {e}")
        raise