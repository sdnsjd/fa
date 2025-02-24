from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from backend.services.admin_service import AdminService
from backend.utils.dependencies import get_db, AsyncSession
from backend.dbase.schemas import ProductUpdate, ProductCreate, CategoryEnum
from typing import Optional, List


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/panel", response_class=HTMLResponse)
async def admin_panel(request: Request, db: AsyncSession = Depends(get_db)):
    return await AdminService.admin_panel(request, db)


@router.delete("/panel/delete_product/{product_id}", response_class=JSONResponse)
async def delete_product(product_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    return await AdminService.delete_product(product_id, request, db)


@router.put("/panel/update_product/{product_id}", response_class=JSONResponse)
async def update_product(product_id: str, product_data: ProductUpdate, request: Request, db: AsyncSession = Depends(get_db)):
    return await AdminService.update_product(product_id, product_data, request, db)


@router.post("/panel/add_product", response_class=JSONResponse)
async def add_product(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    size: Optional[str] = Form(None),
    quantity: int = Form(...),
    category: CategoryEnum = Form(...),
    main_image: UploadFile = File(...),
    images: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db)
):
    return await AdminService.add_product(request, name, price, size, quantity, category, main_image, images, db)

