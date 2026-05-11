from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas.travel import TravelCreate, TravelResponse
from app.services.dependencies import get_db, get_current_user
from app.services import travel as travel_service

router = APIRouter(prefix="/travels", tags=["travels"])


@router.get("", response_model=List[TravelResponse])
def get_travels(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return travel_service.get_travels(db, current_user.id)


@router.post("", response_model=TravelResponse)
def create_travel(data: TravelCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return travel_service.create_travel(db, current_user.id, data)


@router.delete("/{travel_id}")
def delete_travel(travel_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not travel_service.delete_travel(db, travel_id, current_user.id):
        raise HTTPException(status_code=404, detail="여행 기록을 찾을 수 없습니다.")
    return {"message": "삭제되었습니다."}
