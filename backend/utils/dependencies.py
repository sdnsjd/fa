from backend.dbase.database import async_session_factory, AsyncSession
from fastapi import HTTPException, Request
from typing import Optional, List
from backend.dbase.models import UserORM, SessionORM, ProductORM
from sqlalchemy.orm import joinedload
from uuid import UUID
from sqlalchemy import select


async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def get_current_user(request: Request, session: AsyncSession) -> Optional[str]:
    session_id = request.session.get("session_id")
    user_id = request.session.get("user_id")

    if not session_id or not user_id:
        return None

    result = await session.execute(select(SessionORM).where(SessionORM.user_id == user_id))
    get_session = result.scalars().first()

    if get_session:
        user_result = await session.execute(select(UserORM).where(UserORM.id == user_id))
        user = user_result.scalars().first()

        if user:
            return user.role

    return None

