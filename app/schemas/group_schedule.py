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


class ScheduleDetailUpdate(BaseModel):
    confirmed_time: Optional[str] = None
    confirmed_location: Optional[str] = None


class AttendeeAdd(BaseModel):
    user_id: int


class GroupScheduleResponse(BaseModel):
    id: int
    title: str
    confirmed_date: Optional[str] = None
    confirmed_time: Optional[str] = None
    confirmed_location: Optional[str] = None
    attendees: List[int] = []
    availability: Dict[str, List[str]] = {}
    type: str = "meeting"
    duration_days: Optional[int] = None


class AllGroupScheduleResponse(GroupScheduleResponse):
    group_id: int
    group_name: str
