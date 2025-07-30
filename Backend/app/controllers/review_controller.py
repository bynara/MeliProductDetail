from fastapi import APIRouter, Depends, HTTPException
from typing import List

try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..core.security import get_current_user
    from ..repository import get_db
    from ..services.review_service import list_reviews, get_review_by_id, get_reviews_by_key
    from ..schemas.review import ReviewSchema
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from core.security import get_current_user
    from repository import get_db
    from services.review_service import list_reviews, get_review_by_id, get_reviews_by_key
    from schemas.review import ReviewSchema

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.get("/", response_model=List[ReviewSchema])
def get_all_reviews(db=Depends(get_db)):
    return list_reviews(db)

@router.get("/{review_id}", response_model=ReviewSchema)
def get_review(review_id: int, db=Depends(get_db)):
    try:
        return get_review_by_id(db, review_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/product/{product_id}", response_model=List[ReviewSchema])
def get_reviews_by_product(product_id: int, db=Depends(get_db)):
    reviews = get_reviews_by_key(db, "product_id", product_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this product")
    return reviews