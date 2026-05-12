from sqlalchemy.orm import Session
from app.models.travel import Travel
from app.schemas.travel import TravelCreate
from app.services.storage import upload_base64_image, delete_image


def get_travels(db: Session, user_id: int):
    return db.query(Travel).filter(Travel.user_id == user_id).all()


def create_travel(db: Session, user_id: int, data: TravelCreate):
    photo_url = None
    if data.photo:
        photo_url = upload_base64_image(data.photo, folder="travels")

    travel = Travel(user_id=user_id, lat=data.lat, lng=data.lng, name=data.name, photo=photo_url)
    db.add(travel)
    db.commit()
    db.refresh(travel)
    return travel


def delete_travel(db: Session, travel_id: int, user_id: int) -> bool:
    travel = db.query(Travel).filter(Travel.id == travel_id, Travel.user_id == user_id).first()
    if not travel:
        return False
    if travel.photo:
        delete_image(travel.photo)
    db.delete(travel)
    db.commit()
    return True
