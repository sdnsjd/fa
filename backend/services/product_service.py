from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from backend.dbase.models import ProductORM
from backend.utils.dependencies import AsyncSession
from uuid import UUID


class ProductService:
    @staticmethod
    async def get_product_images(product_id: UUID, db: AsyncSession):
        query = select(ProductORM).where(ProductORM.id == product_id).options(joinedload(ProductORM.images))
        result = await db.execute(query)
        product = result.unique().scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        images = [product.main_image] + [image.image_url for image in product.images]
        return {"images": images}

