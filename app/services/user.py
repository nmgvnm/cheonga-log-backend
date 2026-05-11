from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserUpdate
from app.services.auth import hash_password


def update_user(db: Session, user: User, data: UserUpdate) -> User:
    if data.nickname is not None:
        user.nickname = data.nickname  # type: ignore
    if data.phone is not None:
        user.phone = data.phone  # type: ignore
    if data.avatar is not None:
        user.avatar = data.avatar  # type: ignore
    if data.password is not None:
        user.password = hash_password(data.password)  # type: ignore
    db.commit()
    db.refresh(user)
    return user
