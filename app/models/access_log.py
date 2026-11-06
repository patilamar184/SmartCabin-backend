from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class AccessLog(Base):
    __tablename__ = "access_logs"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(
        Integer, ForeignKey("owners.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    visitor_id = Column(
        Integer, ForeignKey("visitors.id", ondelete="SET NULL"),
        nullable=True, index=True
    )

    event_type = Column(String(50), nullable=False)
    authentication_method = Column(String(20), nullable=True)
    result = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("Owner", back_populates="access_logs")
    visitor = relationship("Visitor", back_populates="access_logs")