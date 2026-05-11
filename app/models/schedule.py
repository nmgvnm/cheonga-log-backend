from sqlalchemy import Column, Integer, String, ForeignKey
from app.services.database import Base
from app.models.base import TimestampMixin


class Schedule(TimestampMixin, Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String, nullable=False)
    text = Column(String, nullable=False)
