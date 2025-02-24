import aiofiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from backend.dbase.models import UserORM, CartORM, SessionORM
from backend.utils.dependencies import AsyncSession
from sqlalchemy import select, delete
import bcrypt
from fastapi import Request, HTTPException
import uuid


class AuthService:
    @staticmethod
    async def get_register_form():
        async with aiofiles.open("frontend/templates/register.html", "r", encoding="utf-8") as file:
            content = await file.read()
        return HTMLResponse(content=content, status_code=200)

    @staticmethod
    async def register(db: AsyncSession, username: str, password: str):
        existing_user = await db.execute(select(UserORM).where(UserORM.username == username))
        if existing_user.scalar():
            raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_user = UserORM(username=username, password=hashed_password)
        db.add(new_user)
        await db.flush()

        new_cart = CartORM(user_id=new_user.id)
        db.add(new_cart)
        await db.commit()

        return JSONResponse({"detail": "Регистрация прошла успешна"}, status_code=200)

    @staticmethod
    async def get_login_form():
        async with aiofiles.open("frontend/templates/login.html", "r", encoding="utf-8") as file:
            content = await file.read()
        return HTMLResponse(content=content, status_code=200)

    @staticmethod
    async def login(request: Request, db: AsyncSession, username: str, password: str):
        session_id = request.session.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session["session_id"] = session_id

        result = await db.execute(select(UserORM).where(UserORM.username == username))
        existing_user = result.scalars().first()

        if existing_user and bcrypt.checkpw(password.encode(), existing_user.password.encode()):
            request.session["user_id"] = str(existing_user.id)
            request.session["user_name"] = str(existing_user.username)

            new_session = SessionORM(id=session_id, user_id=existing_user.id)
            db.add(new_session)
            await db.commit()

            return JSONResponse({"message": "Вход выполнен"})

        return JSONResponse({"error": "Неправильный логин или пароль"}, status_code=400)

    @staticmethod
    async def logout(request: Request, db: AsyncSession):
        session_id = request.session.get("session_id")

        if session_id:
            await db.execute(delete(SessionORM).where(SessionORM.id == session_id))
            await db.commit()

        request.session.clear()
        return RedirectResponse(url="/")

