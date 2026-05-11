from pydantic import BaseModel
from typing import Optional


class MeetingCreate(BaseModel):
    title: str
    date: str
    image: Optional[str] = None


class MeetingResponse(BaseModel):
    id: int
    title: str
    date: str
    image: Optional[str] = None

    model_config = {"from_attributes": True}
