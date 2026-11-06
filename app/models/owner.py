from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.database import Base
from sqlalchemy.orm import relationship



class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    phone = Column(String(15), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    visitors = relationship("Visitor", back_populates="owner")

    device = relationship(
    "Device",
    back_populates="owner",
    uselist=False
    )

    access_requests = relationship(
        "AccessRequest",
        back_populates="owner"
    )

    access_logs = relationship(
        "AccessLog",
        back_populates="owner"
    )