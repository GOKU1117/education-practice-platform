from fastapi import APIRouter
from sqlalchemy import select, func
from app.db.session import async_session
from app.models import SolvedTask, Account

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/score")
async def leaderboard():
    async with async_session() as session:
        q = (
            select(
                Account.user_name,
                func.sum(SolvedTask.points).label("total")
            )
            .join(Account, Account.user_id == SolvedTask.user_id)
            .group_by(Account.user_name)
            .order_by(func.sum(SolvedTask.points).desc())
            .limit(10)
        )

        r = await session.execute(q)
        rows = r.all()

        return {"top10": [{"user_name": row[0], "total": row[1]} for row in rows]}
