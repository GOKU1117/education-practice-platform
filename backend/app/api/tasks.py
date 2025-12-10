from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.db.session import async_session
from app.schemas import TaskOut
from app.models import Task, SolvedTask
from app.utils import decode_token 
from sqlalchemy import select


router = APIRouter(prefix="/tasks", tags=["tasks"])


class AnswerCheck(BaseModel):
    task_id: str
    answer: str

@router.get("/list", response_model=list[TaskOut])
async def list_tasks(category: str = None):
    async with async_session() as session:
        q = select(Task)
        if category:
            q = q.where(Task.category == category)
        r = await session.execute(q)
        tasks = r.scalars().all()
        public_tasks = []
        for t in tasks:
            public_tasks.append({
                "task_id": str(t.task_id),
                "title": t.title,
                "description": t.description,
                "hint": t.hint,
                "category": t.category,
                "difficulty": t.difficulty,
                "tags": t.tags,
                "points": t.points,
            })

        return public_tasks

@router.post("/submit")
async def submit_answer(data: AnswerCheck, request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="No token")

    payload = decode_token(token)
    user_id = payload["user_id"]
    async with async_session() as session:
        q = select(Task).where(Task.task_id == data.task_id)
        r = await session.execute(q)
        task = r.scalar_one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        s = select(SolvedTask).where(
            SolvedTask.user_id == user_id,
            SolvedTask.task_id == data.task_id
        )
        solved_r = await session.execute(s)
        solved = solved_r.scalar_one_or_none()

        if solved:
            return {"correct": True, "repeat": True, "points": solved.points}
        
        if task.answer and data.answer.strip() == task.answer.strip():
            new_entry = SolvedTask(
                user_id=user_id,
                task_id=data.task_id,
                points=task.points
            )
            session.add(new_entry)
            await session.commit()

            return {
                "correct": True,
                "points": task.points
            }

        return {"correct": False}
