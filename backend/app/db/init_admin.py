import asyncio
from app.db.session import async_session
from app import crud, utils


async def create_default_admin():
    db = async_session()
    async with db as session:
        existing = await crud.get_account_by_username(session, "admin")
        if existing:
            print("[init] Admin account already exists.")
            return
        password_hash = utils.hash_pass("admin")
        admin_data = {
            "user_name": "admin",
            "user_password": password_hash,
            "permission": 1,
        }
        user = await crud.account_create(session, admin_data)
        await session.commit()
        print("[init] Default admin account created: admin / admin")


if __name__ == "__main__":
    asyncio.run(create_default_admin())
