from sqlalchemy.orm import Session
from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate


def get_schedules(db: Session, user_id: int):
    return db.query(Schedule).filter(Schedule.user_id == user_id).all()


def create_schedule(db: Session, user_id: int, data: ScheduleCreate):
    schedule = Schedule(user_id=user_id, date=data.date, text=data.text)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


def delete_schedule(db: Session, schedule_id: int, user_id: int) -> bool:
    schedule = db.query(Schedule).filter(
        Schedule.id == schedule_id, Schedule.user_id == user_id
    ).first()
    if not schedule:
        return False
    db.delete(schedule)
    db.commit()
    return True
