from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from backend.services.product_service import ProductService
from backend.utils.dependencies import get_db, AsyncSession


router = APIRouter(prefix="/product", tags=["products"])


@router.get("/{product_id}/images", response_class=JSONResponse)
async def get_product_images(product_id: UUID, db: AsyncSession = Depends(get_db)):
    return await ProductService.get_product_images(product_id, db)




