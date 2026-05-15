from sqlalchemy.orm import Session
from app.models.group_schedule import GroupSchedule, GroupScheduleAttendee, GroupScheduleAvailability
from app.models.group import Group, GroupMember
from app.schemas.group_schedule import GroupScheduleCreate


def get_group_schedules(db: Session, group_id: int):
    schedules = db.query(GroupSchedule).filter(GroupSchedule.group_id == group_id).all()
    result = []
    for s in schedules:
        attendees = [
            a.user_id for a in db.query(GroupScheduleAttendee)
            .filter(GroupScheduleAttendee.group_schedule_id == s.id).all()
        ]
        availability: dict = {}
        for row in db.query(GroupScheduleAvailability).filter(
            GroupScheduleAvailability.group_schedule_id == s.id
        ).all():
            key = str(row.user_id)
            availability.setdefault(key, []).append(row.available_date)

        result.append({
            "id": s.id,
            "title": s.title,
            "confirmed_date": s.confirmed_date,
            "confirmed_time": s.confirmed_time,
            "confirmed_location": s.confirmed_location,
            "attendees": attendees,
            "availability": availability,
            "type": s.type or "meeting",
            "duration_days": s.duration_days,
        })
    return result


def create_group_schedule(db: Session, group_id: int, data: GroupScheduleCreate):
    schedule = GroupSchedule(
        group_id=group_id,
        title=data.title,
        type=data.type,
        duration_days=data.duration_days,
    )
    db.add(schedule)
    db.flush()
    for user_id in data.attendees:
        db.add(GroupScheduleAttendee(group_schedule_id=schedule.id, user_id=user_id))
    db.commit()
    db.refresh(schedule)
    return schedule


def update_availability(db: Session, schedule_id: int, member_id: int, available_dates: list):
    db.query(GroupScheduleAvailability).filter(
        GroupScheduleAvailability.group_schedule_id == schedule_id,
        GroupScheduleAvailability.user_id == member_id,
    ).delete()
    for date in available_dates:
        db.add(GroupScheduleAvailability(
            group_schedule_id=schedule_id, user_id=member_id, available_date=date
        ))
    db.commit()


def confirm_date(db: Session, schedule_id: int, confirmed_date: str) -> bool:
    schedule = db.query(GroupSchedule).filter(GroupSchedule.id == schedule_id).first()
    if not schedule:
        return False
    schedule.confirmed_date = confirmed_date  # type: ignore
    db.commit()
    return True


def get_all_group_schedules(db: Session, user_id: int):
    group_ids = (
        db.query(GroupMember.group_id)
        .filter(GroupMember.user_id == user_id)
        .scalar_subquery()
    )
    groups = db.query(Group).filter(Group.id.in_(group_ids)).all()

    result = []
    for group in groups:
        for s in get_group_schedules(db, group.id):
            result.append({**s, "group_id": group.id, "group_name": group.name})
    return result


def update_schedule_detail(db: Session, schedule_id: int, confirmed_time: str | None, confirmed_location: str | None) -> bool:
    schedule = db.query(GroupSchedule).filter(GroupSchedule.id == schedule_id).first()
    if not schedule:
        return False
    setattr(schedule, "confirmed_time", confirmed_time)
    setattr(schedule, "confirmed_location", confirmed_location)
    db.commit()
    return True


def add_schedule_attendee(db: Session, schedule_id: int, user_id: int) -> bool:
    schedule = db.query(GroupSchedule).filter(GroupSchedule.id == schedule_id).first()
    if not schedule:
        return False
    already = db.query(GroupScheduleAttendee).filter(
        GroupScheduleAttendee.group_schedule_id == schedule_id,
        GroupScheduleAttendee.user_id == user_id,
    ).first()
    if already:
        return True
    db.add(GroupScheduleAttendee(group_schedule_id=schedule_id, user_id=user_id))
    db.commit()
    return True


def delete_group_schedule(db: Session, schedule_id: int) -> bool:
    schedule = db.query(GroupSchedule).filter(GroupSchedule.id == schedule_id).first()
    if not schedule:
        return False
    db.query(GroupScheduleAttendee).filter(GroupScheduleAttendee.group_schedule_id == schedule_id).delete(synchronize_session=False)
    db.query(GroupScheduleAvailability).filter(GroupScheduleAvailability.group_schedule_id == schedule_id).delete(synchronize_session=False)
    db.delete(schedule)
    db.commit()
    return True
