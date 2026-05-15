from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.group import GroupCreate, GroupJoin, GroupResponse, MemberResponse, GroupRename, OwnerTransfer
from app.schemas.meeting import MeetingCreate, MeetingResponse
from app.schemas.group_schedule import GroupScheduleCreate, AvailabilityUpdate, ConfirmDate, ScheduleDetailUpdate, AttendeeAdd, GroupScheduleResponse, AllGroupScheduleResponse
from app.services.dependencies import get_db, get_current_user
from app.services import group as group_service
from app.services import meeting as meeting_service
from app.services import group_schedule as group_schedule_service

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=List[GroupResponse])
def get_groups(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return group_service.get_groups(db, current_user.id)


@router.post("", response_model=GroupResponse)
def create_group(data: GroupCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return group_service.create_group(db, current_user.id, data)


@router.get("/schedules", response_model=List[AllGroupScheduleResponse])
def get_all_group_schedules(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return group_schedule_service.get_all_group_schedules(db, current_user.id)


@router.post("/join", response_model=GroupResponse)
def join_group(data: GroupJoin, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    group, error = group_service.join_group(db, current_user.id, data.code)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return group


@router.delete("/{group_id}")
def delete_group(group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not group_service.delete_group(db, group_id, current_user.id):
        raise HTTPException(status_code=404, detail="모임을 찾을 수 없거나 권한이 없습니다.")
    return {"message": "삭제되었습니다."}


@router.patch("/{group_id}")
def rename_group(group_id: int, data: GroupRename, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not group_service.rename_group(db, group_id, current_user.id, data.name):
        raise HTTPException(status_code=403, detail="권한이 없거나 모임을 찾을 수 없습니다.")
    return {"message": "방 이름이 변경되었습니다."}


@router.patch("/{group_id}/transfer")
def transfer_ownership(group_id: int, data: OwnerTransfer, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not group_service.transfer_ownership(db, group_id, current_user.id, data.new_owner_id):
        raise HTTPException(status_code=403, detail="권한이 없거나 대상 멤버가 없습니다.")
    return {"message": "방장이 위임되었습니다."}


@router.delete("/{group_id}/members/{target_id}")
def remove_member(group_id: int, target_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not group_service.remove_member(db, group_id, current_user.id, target_id):
        raise HTTPException(status_code=403, detail="권한이 없거나 멤버를 찾을 수 없습니다.")
    return {"message": "멤버가 삭제되었습니다."}


@router.get("/{group_id}/members", response_model=List[MemberResponse])
def get_members(group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return group_service.get_members(db, group_id)


@router.get("/{group_id}/meetings", response_model=List[MeetingResponse])
def get_meetings(group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return meeting_service.get_meetings(db, group_id)


@router.post("/{group_id}/meetings", response_model=MeetingResponse)
def create_meeting(group_id: int, data: MeetingCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return meeting_service.create_meeting(db, group_id, data)


@router.get("/{group_id}/schedules", response_model=List[GroupScheduleResponse])
def get_group_schedules(group_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return group_schedule_service.get_group_schedules(db, group_id)


@router.post("/{group_id}/schedules")
def create_group_schedule(group_id: int, data: GroupScheduleCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return group_schedule_service.create_group_schedule(db, group_id, data)


@router.patch("/{group_id}/schedules/{schedule_id}/availability")
def update_availability(group_id: int, schedule_id: int, data: AvailabilityUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    group_schedule_service.update_availability(db, schedule_id, data.member_id, data.available_dates)
    return {"message": "업데이트되었습니다."}


@router.patch("/{group_id}/schedules/{schedule_id}/confirm")
def confirm_date(group_id: int, schedule_id: int, data: ConfirmDate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not group_schedule_service.confirm_date(db, schedule_id, data.confirmed_date):
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")
    return {"message": "날짜가 확정되었습니다."}


@router.patch("/{group_id}/schedules/{schedule_id}/detail")
def update_schedule_detail(group_id: int, schedule_id: int, data: ScheduleDetailUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not group_schedule_service.update_schedule_detail(db, schedule_id, data.confirmed_time, data.confirmed_location):
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")
    return {"message": "업데이트되었습니다."}


@router.post("/{group_id}/schedules/{schedule_id}/attendees")
def add_schedule_attendee(group_id: int, schedule_id: int, data: AttendeeAdd, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not group_schedule_service.add_schedule_attendee(db, schedule_id, data.user_id):
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")
    return {"message": "멤버가 추가되었습니다."}


@router.delete("/{group_id}/schedules/{schedule_id}")
def delete_group_schedule(group_id: int, schedule_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not group_schedule_service.delete_group_schedule(db, schedule_id):
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")
    return {"message": "삭제되었습니다."}
