from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from backend.services.cart_service import CartService
from backend.utils.dependencies import get_db, AsyncSession

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/", response_class=HTMLResponse)
async def get_cart(request: Request, db: AsyncSession = Depends(get_db)):
    return await CartService.get_cart(request, db)


@router.post("/add_to_cart", response_class=JSONResponse)
async def add_to_cart(request: Request):
    return await CartService.add_to_cart(request)


@router.post("/increase", response_class=JSONResponse)
async def increase_quantity(request: Request):
    return await CartService.increase_quantity(request)


@router.post("/decrease", response_class=JSONResponse)
async def decrease_quantity(request: Request):
    return await CartService.decrease_quantity(request)


@router.post("/remove", response_class=JSONResponse)
async def remove_product(request: Request):
    return await CartService.remove_product(request)


