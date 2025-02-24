import os
import shutil
from backend.conf import templates, UPLOAD_DIRECTORY
from backend.dbase.models import ProductORM, ImageORM
from backend.dbase.schemas import ProductUpdate, CategoryEnum
from backend.utils.dependencies import get_current_user, AsyncSession
from fastapi import HTTPException, Request, status, UploadFile
from sqlalchemy import select
from fastapi.responses import JSONResponse
from typing import Optional, List
import uuid


class AdminService:
    @staticmethod
    async def admin_panel(request: Request, db: AsyncSession):
        current_user = await get_current_user(request, db)
        if not current_user or current_user != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        products = await db.execute(select(ProductORM))
        products = products.scalars().all()

        return templates.TemplateResponse("admin_panel.html", {
            "request": request,
            "products": products,
        })

    @staticmethod
    async def delete_product(product_id: str, request: Request, db: AsyncSession):
        current_user = await get_current_user(request, db)
        if not current_user or current_user != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        product = await db.get(ProductORM, product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

        await db.delete(product)
        await db.commit()

        return JSONResponse(content={"message": "Product successfully deleted"})

    @staticmethod
    async def update_product(product_id: str, product_data: ProductUpdate, request: Request, db: AsyncSession):
        current_user = await get_current_user(request, db)
        if not current_user or current_user != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        result = await db.execute(select(ProductORM).filter(ProductORM.id == product_id))
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product.name = product_data.name
        product.price = product_data.price
        product.size = product_data.size
        product.main_image = product_data.main_image
        product.quantity = product_data.quantity
        product.category = product_data.category

        await db.commit()
        return {"message": "Product updated successfully"}

    @staticmethod
    async def add_product(
        request: Request,
        name: str,
        price: float,
        size: Optional[str],
        quantity: int,
        category: CategoryEnum,
        main_image: UploadFile,
        images: List[UploadFile],
        db: AsyncSession
    ):
        current_user = await get_current_user(request, db)
        if not current_user or current_user != 'admin':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access forbidden")

        try:
            main_image_path = os.path.join(UPLOAD_DIRECTORY, main_image.filename)
            with open(main_image_path, "wb") as buffer:
                shutil.copyfileobj(main_image.file, buffer)

            new_product = ProductORM(
                id=str(uuid.uuid4()),
                name=name,
                price=price,
                size=size,
                main_image=f"/{main_image_path}",
                quantity=quantity,
                category=category
            )

            db.add(new_product)
            await db.flush()

            for image in images:
                image_path = os.path.join(UPLOAD_DIRECTORY, image.filename)
                with open(image_path, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)

                new_image = ImageORM(
                    image_url=f"/{image_path}",
                    product_id=new_product.id
                )
                db.add(new_image)
                print(f"Image {new_image.id} added for product {new_product.id} with path {image_path}")

            await db.commit()
        except Exception as e:
            await db.rollback()
            return {"error": str(e)}
        return {"message": "Product added successfully"}