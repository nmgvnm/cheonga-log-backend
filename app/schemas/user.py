from pydantic import BaseModel, field_validator
from typing import Optional


class UserCreate(BaseModel):
    user_id: str
    nickname: str
    password: str
    phone: str
    avatar: int = 1

    @field_validator("avatar")
    @classmethod
    def avatar_range(cls, v: int) -> int:
        if not 1 <= v <= 6:
            raise ValueError("avatar는 1~6 사이의 값이어야 합니다.")
        return v


class UserLogin(BaseModel):
    user_id: str
    password: str


class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    phone: Optional[str] = None
    avatar: Optional[int] = None
    password: Optional[str] = None

    @field_validator("avatar")
    @classmethod
    def avatar_range(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not 1 <= v <= 6:
            raise ValueError("avatar는 1~6 사이의 값이어야 합니다.")
        return v


class UserResponse(BaseModel):
    id: int
    user_id: str
    nickname: str
    phone: str
    avatar: int

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
