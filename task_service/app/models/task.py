from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    auth_user_id = Column(Integer, nullable=False)
    title = Column(String, nullable = False)
    description = Column(Text)
    status = Column(String, default = "pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())