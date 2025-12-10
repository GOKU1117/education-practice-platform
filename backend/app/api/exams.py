from fastapi import APIRouter, Depends, HTTPException, Header, Request
from typing import List
from app.schemas import ExamCreate, ExamOut
from app.db.session import async_session
from app import crud, utils


router = APIRouter(prefix="/exams", tags=["exams"])

def get_user_from_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="missing token")
    token = authorization.split(" ")[1]
    payload = utils.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="invalid token")
    return payload

@router.post("/", response_model=dict)
async def submit_exam(exam: ExamCreate, user=Depends(get_user_from_token)):
    db = async_session()
    created = await crud.create_exam(db, user_id=user.get("user_id"), exam=exam)
    return {"status": "ok", "exam_id": created.id}
