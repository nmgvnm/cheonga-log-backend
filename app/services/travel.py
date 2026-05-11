from sqlalchemy.orm import Session
from app.models.travel import Travel
from app.schemas.travel import TravelCreate


def get_travels(db: Session, user_id: int):
    return db.query(Travel).filter(Travel.user_id == user_id).all()


def create_travel(db: Session, user_id: int, data: TravelCreate):
    travel = Travel(user_id=user_id, lat=data.lat, lng=data.lng, name=data.name, photo=data.photo)
    db.add(travel)
    db.commit()
    db.refresh(travel)
    return travel


def delete_travel(db: Session, travel_id: int, user_id: int) -> bool:
    travel = db.query(Travel).filter(Travel.id == travel_id, Travel.user_id == user_id).first()
    if not travel:
        return False
    db.delete(travel)
    db.commit()
    return True
