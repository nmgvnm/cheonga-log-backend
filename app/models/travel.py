from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from app.services.database import Base
from app.models.base import TimestampMixin


class Travel(TimestampMixin, Base):
    __tablename__ = "travels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    name = Column(String, nullable=False)
    photo = Column(Text, nullable=True)
