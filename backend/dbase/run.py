import asyncio
from backend.dbase.orm import AsyncORM


async def main():
    # await AsyncORM.create_tables()
    # await AsyncORM.insert_products()
    await AsyncORM.update_user_role(username='admin', new_role='admin')

asyncio.run(main())
