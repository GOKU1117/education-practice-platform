from fastapi import (APIRouter,Depends,UploadFile,File,Form,HTTPException,Header,)
from app.db.session import async_session
from app.models import Exam, Task
from app.schemas import TaskOut
from app.utils import decode_token
from datetime import datetime
import os
import uuid
from sqlalchemy import delete

router = APIRouter(prefix="/admin", tags=["admin"])

UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def admin_check(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="missing token")
    try:
        token = authorization.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="invalid header")
    payload = decode_token(token)
    if not payload or payload.get("sub") != "admin":
        raise HTTPException(status_code=403, detail="admin only")
    return payload

@router.post("/exam/create")
async def create_exam(
    user_id: str = Form(...),
    exam_id: str = Form(...),
    exam_name: str = Form(...),
    exam_score: int = Form(...),
    user=Depends(admin_check),
):
    async with async_session() as session:
        db_exam = Exam(
            user_id=user_id,
            exam_id=exam_id,
            exam_name=exam_name,
            exam_score=exam_score,
            created_at=datetime.utcnow(),
        )
        session.add(db_exam)
        await session.commit()
        await session.refresh(db_exam)
        return db_exam


@router.post("/tasks/create", response_model=TaskOut)
async def create_task(
    title: str = Form(...),
    description: str = Form(None),
    category: str = Form(None),
    difficulty: str = Form("Easy"),
    tags: str = Form(""),
    points: int = Form(0),
    answer: str = Form(None),
    hint: str = Form(None),

    user=Depends(admin_check),
):
    tags_list = [t.strip() for t in tags.split(",") if t.strip()]
    async with async_session() as session:
        db_task = Task(
            task_id=uuid.uuid4(),
            title=title,
            description=description,
            category=category,
            difficulty=difficulty,
            tags=tags_list,
            points=points,
            answer=answer,
            hint=hint,
            created_at=datetime.utcnow(),
        )
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return db_task

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str, user=Depends(admin_check)):
    async with async_session() as session:
        q = delete(Task).where(Task.task_id == task_id)
        await session.execute(q)
        await session.commit()
        return {"status": "deleted"}