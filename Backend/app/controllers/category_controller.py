from fastapi import APIRouter, Depends, HTTPException
from typing import List

try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from ..core.security import get_current_user
    from ..repository import get_db
    from ..services.category_service import list_categories, get_category_by_id
    from ..schemas.category import CategorySchema
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from core.security import get_current_user
    from repository import get_db
    from services.category_service import list_categories, get_category_by_id
    from schemas.category import CategorySchema

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[CategorySchema])
def get_all_categories(db=Depends(get_db)):
    return list_categories(db)

@router.get("/{category_id}", response_model=CategorySchema)
def get_category(category_id: int, db=Depends(get_db)):
    try:
        return get_category_by_id(db, category_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))