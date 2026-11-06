from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class AccessRequest(Base):
    __tablename__ = "access_requests"

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(
        Integer, ForeignKey("owners.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    visitor_id = Column(
        Integer, ForeignKey("visitors.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    authentication_method = Column(String(20), nullable=False)
    status = Column(String(20), default="pending", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    responded_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("Owner", back_populates="access_requests")
    visitor = relationship("Visitor", back_populates="access_requests")