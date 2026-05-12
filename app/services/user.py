from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserUpdate
from app.services.auth import hash_password


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    if data.nickname is not None:
        dup = db.query(User).filter(User.nickname == data.nickname, User.id != user.id).first()
        if dup:
            raise ValueError("이미 사용 중인 닉네임입니다.")
        user.nickname = data.nickname  # type: ignore
    if data.phone is not None:
        dup = db.query(User).filter(User.phone == data.phone, User.id != user.id).first()
        if dup:
            raise ValueError("이미 등록된 휴대폰 번호입니다.")
        user.phone = data.phone  # type: ignore
    if data.avatar is not None:
        user.avatar = data.avatar  # type: ignore
    if data.password is not None:
        user.password = hash_password(data.password)  # type: ignore
    db.commit()
    db.refresh(user)
    return user
