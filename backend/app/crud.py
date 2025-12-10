from datetime import datetime
from sqlalchemy import select, func
from app.models import Account, Exam, Task, TrafficLog
from app.schemas import AccountCreate
from app.utils import hash_pass


async def account_create(db, account):
    async with db as session:
        if isinstance(account, dict):
            user_name = account.get("user_name")
            user_email = account.get("user_email")
            user_password = account.get("user_password")
            permission = account.get("permission", 0)
        else:
            user_name = account.user_name
            user_email = getattr(account, "user_email", None)
            user_password = hash_pass(account.password)
            permission = 0

        db_user = Account(
            user_name=user_name,
            user_email=user_email,
            user_password=user_password,
            permission=permission,
            signed_up_time=datetime.utcnow(),
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user


async def get_account_by_username(db, username: str):
    async with db as session:
        q = select(Account).where(Account.user_name == username)
        r = await session.execute(q)
        return r.scalars().first()


async def get_account_by_userid(db, user_id):
    async with db as session:
        q = select(Account).where(Account.user_id == user_id)
        r = await session.execute(q)
        return r.scalars().first()


async def get_leaderboard(db, limit: int = 10):
    async with db as session:
        q = (
            select(Exam.user_id, func.sum(Exam.exam_score).label("total"))
            .group_by(Exam.user_id)
            .order_by(func.sum(Exam.exam_score).desc())
            .limit(limit)
        )
        r = await session.execute(q)
        return r.all()

async def get_task(db, task_id: str):

    async with db as session:
        q = select(Task).where(Task.task_id == task_id)
        r = await session.execute(q)
        return r.scalars().first()
    
async def log_traffic(db, user_id, path: str, method: str):
    async with db as session:
        entry = TrafficLog(
            user_id=user_id,
            path=path,
            method=method,
            created_at=datetime.utcnow(),
        )
        session.add(entry)
        await session.commit()
