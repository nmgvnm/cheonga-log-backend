from sqlalchemy import Column, Integer, String, ForeignKey
from app.services.database import Base
from app.models.base import TimestampMixin


class Group(TimestampMixin, Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String(6), unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)


class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
