from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str


class GroupJoin(BaseModel):
    code: str


class GroupRename(BaseModel):
    name: str


class OwnerTransfer(BaseModel):
    new_owner_id: int


class GroupResponse(BaseModel):
    id: int
    name: str
    code: str
    owner_id: int

    model_config = {"from_attributes": True}


class MemberResponse(BaseModel):
    id: int
    user_id: str
    nickname: str
    avatar: int

    model_config = {"from_attributes": True}
