from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import ValidationError
from backend.dbase.schemas import UserRegistration
from backend.services.auth_service import AuthService
from backend.utils.dependencies import get_db, AsyncSession
from fastapi import APIRouter, Depends, Form, Request, HTTPException


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/register", response_class=HTMLResponse)
async def get_register_form():
    return await AuthService.get_register_form()


@router.post("/register", response_class=JSONResponse)
async def register(user: UserRegistration, db: AsyncSession = Depends(get_db)):
    try:
        return await AuthService.register(db, user.username, user.password)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())


@router.get("/login", response_class=HTMLResponse)
async def get_login_form():
    return await AuthService.get_login_form()


@router.post("/login", response_class=JSONResponse)
async def login(request: Request,
                username: str = Form(...),
                password: str = Form(...),
                db: AsyncSession = Depends(get_db)):
    return await AuthService.login(request, db, username, password)


@router.post("/logout", response_class=JSONResponse)
async def logout(request: Request, db: AsyncSession = Depends(get_db)):
    return await AuthService.logout(request, db)
