from fastapi import FastAPI, Request, APIRouter
from app.api import admin, auth, exams, tasks, leaderboard
from app.db.session import engine
from app.db.session import async_session
from app.db.base import Base
from app.utils import decode_token


app = FastAPI(title="ctf-backend")

api_router = APIRouter(prefix="/api")

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(exams.router)
app.include_router(tasks.router) 
app.include_router(leaderboard.router)

@app.on_event("startup")

async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    try:
        token = request.headers.get("Authorization")
        user_id = None
        if token and token.startswith("Bearer "):
            from app.utils import decode_token
            p = decode_token(token.split(" ")[1])
            if p:
                user_id = p.get("user_id")
        async with async_session() as db:
            from app import crud
            await crud.log_traffic(db, user_id, request.url.path, request.method)
    except Exception as e:
        print(f"[log_requests] error: {e}")  
    return response

async def crud_log(db, user_id, path, method):
    from app import crud
    await crud.log_traffic(db, user_id, path, method)
