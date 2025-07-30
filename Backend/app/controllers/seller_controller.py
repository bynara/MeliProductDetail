from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..core.security import get_current_user
    from ..repository import get_db
    from ..services.seller_service import list_sellers, get_seller_by_id
    from ..schemas.seller import SellerSchema
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from core.security import get_current_user
    from repository import get_db
    from services.seller_service import list_sellers, get_seller_by_id
    from schemas.seller import SellerSchema

router = APIRouter(prefix="/sellers", tags=["Sellers"])

@router.get("/", response_model=List[SellerSchema])
def get_all_sellers(db=Depends(get_db)):
    try:
        return list_sellers(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving sellers: {str(e)}"
        )

@router.get("/{seller_id}", response_model=SellerSchema)
def get_seller(seller_id: int, db=Depends(get_db)):
    try:
        seller = get_seller_by_id(db, seller_id)
        if not seller:
            raise HTTPException(status_code=404, detail="Seller not found")
        return seller
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving seller: {str(e)}"
        )