from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.dependencies import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.signup(db, user)


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = auth_service.login(db, user.user_id, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")
    return {"access_token": token, "token_type": "bearer"}
