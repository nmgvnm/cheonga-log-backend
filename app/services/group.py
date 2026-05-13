import random
import string
from sqlalchemy.orm import Session
from app.models.group import Group, GroupMember
from app.models.group_schedule import (
    GroupSchedule,
    GroupScheduleAttendee,
    GroupScheduleAvailability,
)
from app.models.meeting import Meeting
from app.models.user import User
from app.schemas.group import GroupCreate


def _generate_code(db: Session) -> str:
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not db.query(Group).filter(Group.code == code).first():
            return code


def get_groups(db: Session, user_id: int):
    group_ids = (
        db.query(GroupMember.group_id)
        .filter(GroupMember.user_id == user_id)
        .scalar_subquery()
    )
    return db.query(Group).filter(Group.id.in_(group_ids)).all()


def create_group(db: Session, user_id: int, data: GroupCreate):
    group = Group(name=data.name, code=_generate_code(db), owner_id=user_id)
    db.add(group)
    db.flush()
    db.add(GroupMember(group_id=group.id, user_id=user_id))
    db.commit()
    db.refresh(group)
    return group


def join_group(db: Session, user_id: int, code: str):
    group = db.query(Group).filter(Group.code == code).first()
    if not group:
        return None, "존재하지 않는 모임 코드입니다."

    already = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group.id, GroupMember.user_id == user_id)
        .first()
    )
    if already:
        return None, "이미 참여 중인 모임입니다."

    db.add(GroupMember(group_id=group.id, user_id=user_id))
    db.commit()
    return group, None


def delete_group(db: Session, group_id: int, user_id: int) -> bool:
    group = (
        db.query(Group).filter(Group.id == group_id, Group.owner_id == user_id).first()
    )
    if not group:
        return False

    schedule_ids = [
        s.id
        for s in db.query(GroupSchedule)
        .filter(GroupSchedule.group_id == group_id)
        .all()
    ]
    if schedule_ids:
        db.query(GroupScheduleAttendee).filter(
            GroupScheduleAttendee.group_schedule_id.in_(schedule_ids)
        ).delete(synchronize_session=False)
        db.query(GroupScheduleAvailability).filter(
            GroupScheduleAvailability.group_schedule_id.in_(schedule_ids)
        ).delete(synchronize_session=False)
        db.query(GroupSchedule).filter(GroupSchedule.group_id == group_id).delete(
            synchronize_session=False
        )

    db.query(Meeting).filter(Meeting.group_id == group_id).delete(
        synchronize_session=False
    )
    db.query(GroupMember).filter(GroupMember.group_id == group_id).delete(
        synchronize_session=False
    )
    db.delete(group)
    db.commit()
    return True


def get_members(db: Session, group_id: int):
    user_ids = (
        db.query(GroupMember.user_id)
        .filter(GroupMember.group_id == group_id)
        .scalar_subquery()
    )
    return db.query(User).filter(User.id.in_(user_ids)).all()


def rename_group(db: Session, group_id: int, user_id: int, new_name: str) -> bool:
    group = (
        db.query(Group).filter(Group.id == group_id, Group.owner_id == user_id).first()
    )
    if not group:
        return False
    setattr(group, "name", new_name)
    db.commit()
    return True


def transfer_ownership(
    db: Session, group_id: int, user_id: int, new_owner_id: int
) -> bool:
    group = (
        db.query(Group).filter(Group.id == group_id, Group.owner_id == user_id).first()
    )
    if not group:
        return False
    is_member = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id, GroupMember.user_id == new_owner_id)
        .first()
    )
    if not is_member:
        return False
    setattr(group, "owner_id", new_owner_id)
    db.commit()
    return True


def remove_member(
    db: Session, group_id: int, owner_user_id: int, target_user_id: int
) -> bool:
    group = (
        db.query(Group)
        .filter(Group.id == group_id, Group.owner_id == owner_user_id)
        .first()
    )
    if not group:
        return False
    if target_user_id == owner_user_id:
        return False
    deleted = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id, GroupMember.user_id == target_user_id)
        .delete()
    )
    db.commit()
    return deleted > 0
