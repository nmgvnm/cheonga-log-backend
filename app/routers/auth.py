from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import os

from app.services.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services import auth as auth_service
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY: str = os.getenv("SECRET_KEY") or ""
ALGORITHM = os.getenv("ALGORITHM", "HS256")


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return auth_service.signup(db, user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    tokens = auth_service.login(db, user.user_id, user.password)
    if not tokens:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")
    return {**tokens, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: dict, db: Session = Depends(get_db)):
    refresh_token = body.get("refresh_token", "")
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="유효하지 않은 refresh 토큰입니다.")
        user_id = str(payload.get("sub", ""))
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 refresh 토큰입니다.")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")

    new_payload = {"sub": user.user_id}
    return {
        "access_token": auth_service.create_access_token(new_payload),
        "refresh_token": auth_service.create_refresh_token(new_payload),
        "token_type": "bearer",
    }
