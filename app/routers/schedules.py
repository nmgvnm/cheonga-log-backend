from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.schedule import ScheduleCreate, ScheduleResponse
from app.services.dependencies import get_db, get_current_user
from app.services import schedule as schedule_service

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("", response_model=List[ScheduleResponse])
def get_schedules(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return schedule_service.get_schedules(db, current_user.id)


@router.post("", response_model=ScheduleResponse)
def create_schedule(data: ScheduleCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return schedule_service.create_schedule(db, current_user.id, data)


@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not schedule_service.delete_schedule(db, schedule_id, current_user.id):
        raise HTTPException(status_code=404, detail="일정을 찾을 수 없습니다.")
    return {"message": "삭제되었습니다."}
