from sqlalchemy import text, update
from backend.dbase.database import async_engine, Base, async_session_factory
from backend.dbase.models import ProductORM, ImageORM, CategoryEnum, UserORM


class AsyncORM:

    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_products():
        async with async_session_factory() as session:
            product1 = ProductORM(name='sockse4', price=19.5,category=CategoryEnum.SOCKS, main_image='/frontend/static/images/2.jpg', quantity=1)
            product2 = ProductORM(name='bitcoin', price=24.5,category=CategoryEnum.TSHIRT, main_image='/frontend/static/images/bitcoin.jpg', size='XL',quantity=1)
            product3 = ProductORM(name='popcat', price=24.5,category=CategoryEnum.TSHIRT, main_image='/frontend/static/images/popcat.jpg', size='XL',quantity=1)
            product4 = ProductORM(name='retardio', price=24.5,category=CategoryEnum.TSHIRT,main_image='/frontend/static/images/retardio.jpg',size='XL',quantity=1)

            tshirt2 = ImageORM(image_url='/frontend/static/images/image2.jpg', product=product1)
            bitcoin2 = ImageORM(image_url='/frontend/static/images/image2.jpg', product=product2)
            popcat2 = ImageORM(image_url='/frontend/static/images/image2.jpg', product=product3)
            retardio2 = ImageORM(image_url='/frontend/static/images/image2.jpg', product=product4)

            session.add_all([product1, product2, product3, product4])
            session.add_all([tshirt2, bitcoin2, popcat2, retardio2])
            await session.flush()
            await session.commit()

    @staticmethod
    async def update_user_role(username: str, new_role: str):
        async with async_session_factory() as session:
            stmt = update(UserORM).where(UserORM.username == username).values(role=new_role)
            await session.execute(stmt)
            await session.commit()









