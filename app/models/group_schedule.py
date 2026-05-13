from sqlalchemy import Column, Integer, String, ForeignKey
from app.services.database import Base


class GroupSchedule(Base):
    __tablename__ = "group_schedules"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    title = Column(String, nullable=False)
    confirmed_date = Column(String, nullable=True)
    confirmed_time = Column(String, nullable=True)
    confirmed_location = Column(String, nullable=True)
    type = Column(String, nullable=False, default="meeting")
    duration_days = Column(Integer, nullable=True)


class GroupScheduleAttendee(Base):
    __tablename__ = "group_schedule_attendees"

    id = Column(Integer, primary_key=True, index=True)
    group_schedule_id = Column(Integer, ForeignKey("group_schedules.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class GroupScheduleAvailability(Base):
    __tablename__ = "group_schedule_availability"

    id = Column(Integer, primary_key=True, index=True)
    group_schedule_id = Column(Integer, ForeignKey("group_schedules.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    available_date = Column(String, nullable=False)
