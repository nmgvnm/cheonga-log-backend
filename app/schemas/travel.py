from pydantic import BaseModel
from typing import Optional


class TravelCreate(BaseModel):
    lat: float
    lng: float
    name: str
    photo: Optional[str] = None


class TravelResponse(BaseModel):
    id: int
    lat: float
    lng: float
    name: str
    photo: Optional[str] = None

    model_config = {"from_attributes": True}
