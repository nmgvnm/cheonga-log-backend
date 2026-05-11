from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.services.database import Base
from app.models.base import TimestampMixin


class Meeting(TimestampMixin, Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    title = Column(String, nullable=False)
    date = Column(String, nullable=False)
    image = Column(Text, nullable=True)
