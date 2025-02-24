from backend.dbase.config import DATABASE_URL_asyncpg
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

async_engine = create_async_engine(
    url=DATABASE_URL_asyncpg,
    echo=False,
)

async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


