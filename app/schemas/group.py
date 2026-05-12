from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str


class GroupJoin(BaseModel):
    code: str


class GroupResponse(BaseModel):
    id: int
    name: str
    code: str

    model_config = {"from_attributes": True}


class MemberResponse(BaseModel):
    id: int
    user_id: str
    nickname: str
    avatar: int

    model_config = {"from_attributes": True}
