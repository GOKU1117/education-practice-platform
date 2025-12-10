from sqlalchemy import (Column,String,Integer,Text,DateTime,ForeignKey,ARRAY,)
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid
from datetime import datetime


class Account(Base):
    __tablename__ = "account"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = Column(String, unique=True, nullable=False)
    user_email = Column(String, unique=True)
    user_password = Column(String, nullable=False)
    permission = Column(Integer, default=0)
    signed_up_time = Column(DateTime, default=datetime.utcnow)


class Exam(Base):
    __tablename__ = "exam"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("account.user_id"))
    exam_id = Column(String, nullable=False)
    exam_name = Column(String, nullable=False)
    exam_score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "task"

    task_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    answer = Column(String, nullable=True)
    hint = Column(Text, nullable=True)
    category = Column(String)
    difficulty = Column(String, default="Easy")
    tags = Column(ARRAY(String))
    points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class SolvedTask(Base):
    __tablename__ = "solved_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("account.user_id"))
    task_id = Column(UUID(as_uuid=True), ForeignKey("task.task_id"))
    points = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class TrafficLog(Base):
    __tablename__ = "traffic_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    path = Column(String)
    method = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
