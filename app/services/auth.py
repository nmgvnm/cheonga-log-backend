import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.models.user import User
from app.schemas.user import UserCreate

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = 30


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def signup(db: Session, user: UserCreate) -> User:
    if db.query(User).filter(User.user_id == user.user_id).first():
        raise ValueError("이미 사용 중인 아이디입니다.")
    if db.query(User).filter(User.nickname == user.nickname).first():
        raise ValueError("이미 사용 중인 닉네임입니다.")
    if db.query(User).filter(User.phone == user.phone).first():
        raise ValueError("이미 등록된 휴대폰 번호입니다.")

    db_user = User(
        user_id=user.user_id,
        nickname=user.nickname,
        password=hash_password(user.password),
        phone=user.phone,
        avatar=user.avatar,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(db: Session, user_id: str, password: str) -> dict | None:
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user or not verify_password(password, user.password):
        return None
    payload = {"sub": user.user_id}
    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
    }
