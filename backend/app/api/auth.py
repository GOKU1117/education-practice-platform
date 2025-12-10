from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.schemas import AccountCreate, Token
from app.db.session import async_session
from app import crud, utils

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=dict)
async def register(account: AccountCreate):
    if account.user_name.lower() == "admin":
        raise HTTPException(status_code=403, detail="cannot create admin account")

    db = async_session()
    existing = await crud.get_account_by_username(db, account.user_name)
    if existing:
        raise HTTPException(status_code=400, detail="username exists")

    user = await crud.account_create(db, account)
    return {"user_id": str(user.user_id), "user_name": user.user_name}


@router.post("/token", response_model=Token)
async def login(form: AccountCreate):
    db = async_session()
    user = await crud.get_account_by_username(db, form.user_name)
    if not user:
        raise HTTPException(status_code=400, detail="incorrect username")
    if not utils.verify_pass(form.password, user.user_password):
        raise HTTPException(status_code=400, detail="incorrect password")
    token = utils.create_access_token(
        {
            "sub": user.user_name,
            "user_id": str(user.user_id),
            "permission": user.permission,
        }
    )
    force_change = (
        user.user_name == "admin"
        and utils.verify_pass("admin", user.user_password)
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "force_password_change": force_change,
    }
