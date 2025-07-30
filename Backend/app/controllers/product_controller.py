from fastapi import APIRouter, Depends, HTTPException
from typing import List

try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..core.security import get_current_user
    from ..repository import get_db
    from ..services.product_service import list_products, get_product_by_id, get_similar_products
    from ..schemas.product import ProductSchema
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from core.security import get_current_user
    from repository import get_db
    from services.product_service import list_products, get_product_by_id, get_similar_products
    from schemas.product import ProductSchema

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[ProductSchema])
def get_all_products(db=Depends(get_db)):
    return list_products(db)

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db=Depends(get_db)):
    try:
        return get_product_by_id(db, product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/{product_id}/similar/", response_model=List[ProductSchema], tags=["Products"])
async def get_similar_products_endpoint(product_id: int, db=Depends(get_db), limit: int = 4):
    try:
        return get_similar_products(db, product_id, limit)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))