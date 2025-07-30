from fastapi import APIRouter, Depends, HTTPException
from typing import List

try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..core.security import get_current_user
    from ..repository import get_db
    from ..services.payment_method_service import list_payment_methods, get_payment_method_by_id
    from ..schemas.payment_method import PaymentMethodSchema
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from core.security import get_current_user
    from repository import get_db
    from services.payment_method_service import list_payment_methods, get_payment_method_by_id
    from schemas.payment_method import PaymentMethodSchema

router = APIRouter(prefix="/payment-methods", tags=["Payment Methods"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=List[PaymentMethodSchema])
def get_all_payment_methods(db=Depends(get_db)):
    return list_payment_methods(db)

@router.get("/{payment_method_id}", response_model=PaymentMethodSchema)
def get_payment_method(payment_method_id: int, db=Depends(get_db)):
    try:
        return get_payment_method_by_id(db, payment_method_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))