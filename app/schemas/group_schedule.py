from pydantic import BaseModel
from typing import Optional, List, Dict


class GroupScheduleCreate(BaseModel):
    title: str
    attendees: List[int]
    type: str = "meeting"
    duration_days: Optional[int] = None


class AvailabilityUpdate(BaseModel):
    member_id: int
    available_dates: List[str]


class ConfirmDate(BaseModel):
    confirmed_date: str


class GroupScheduleResponse(BaseModel):
    id: int
    title: str
    confirmed_date: Optional[str] = None
    attendees: List[int] = []
    availability: Dict[str, List[str]] = {}
    type: str = "meeting"
    duration_days: Optional[int] = None
