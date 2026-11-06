from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    __table_args__ = (
        UniqueConstraint(
            "owner_id", "fingerprint_id",
            name="uq_owner_fingerprint"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    owner_id = Column(
        Integer, ForeignKey("owners.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=False)
    role = Column(String(20), nullable=False)

    pin_hash = Column(String(255), nullable=False)

    fingerprint_id = Column(Integer, nullable=True)
    fingerprint_enrolled = Column(Boolean, default=False, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("Owner", back_populates="visitors")
    access_requests = relationship(
        "AccessRequest", back_populates="visitor"
    )
    access_logs = relationship("AccessLog", back_populates="visitor")