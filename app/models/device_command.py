from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, JSON
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.database import Base


class DeviceCommand(Base):
    __tablename__ = "device_commands"

    id = Column(Integer, primary_key=True, index=True)

    device_id = Column(
        Integer, ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False, index=True
    )

    command_type = Column(String(50), nullable=False)
    payload = Column(JSON, nullable=True)

    status = Column(String(20), default="pending", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    acknowledged_at = Column(DateTime(timezone=True), nullable=True)

    device = relationship("Device", back_populates="commands")