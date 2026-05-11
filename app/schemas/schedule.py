from pydantic import BaseModel


class ScheduleCreate(BaseModel):
    date: str
    text: str


class ScheduleResponse(BaseModel):
    id: int
    date: str
    text: str

    model_config = {"from_attributes": True}
