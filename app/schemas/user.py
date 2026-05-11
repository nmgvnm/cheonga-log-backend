from pydantic import BaseModel


class UserCreate(BaseModel):
    user_id: str
    nickname: str
    password: str
    phone: str


class UserLogin(BaseModel):
    user_id: str
    password: str


class UserResponse(BaseModel):
    id: int
    user_id: str
    nickname: str
    phone: str

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
