from sqlalchemy.orm import Session
from app.models.meeting import Meeting
from app.schemas.meeting import MeetingCreate


def get_meetings(db: Session, group_id: int):
    return db.query(Meeting).filter(Meeting.group_id == group_id).all()


def create_meeting(db: Session, group_id: int, data: MeetingCreate):
    meeting = Meeting(group_id=group_id, title=data.title, date=data.date, image=data.image)
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting
