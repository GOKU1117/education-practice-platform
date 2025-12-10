from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID


class AccountCreate(BaseModel):
    user_name: str
    user_email: Optional[EmailStr]
    password: str


class AccountOut(BaseModel):
    user_id: UUID
    user_name: str
    user_email: Optional[EmailStr]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_name: Optional[str] = None


class ExamCreate(BaseModel):
    exam_id: str
    exam_name: str
    exam_score: int


class ExamOut(BaseModel):
    id: int
    user_id: UUID
    exam_id: str
    exam_name: str
    exam_score: int


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    answer: Optional[str]
    hint: Optional[str]
    category: Optional[str]
    difficulty: Optional[str] = "Easy"
    tags: Optional[List[str]] = []
    points: int = 0

class TaskOut(BaseModel):
    task_id: UUID
    title: str
    description: Optional[str]
    answer: Optional[str] = None
    hint: Optional[str] = None
    category: Optional[str]
    difficulty: str
    tags: Optional[List[str]]
    points: int

    class Config:
            orm_mode = True