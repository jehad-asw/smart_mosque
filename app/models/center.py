from sqlalchemy import Column, Integer, ForeignKey, String, Enum, Text
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum
from datetime import datetime


class CenterStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    under_maintenance = "under_maintenance"


class Center(Base):
    __tablename__ = "centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    status = Column(Enum(CenterStatus), default=CenterStatus.active)
    manager_id = Column(Integer, ForeignKey("users.id"))
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    capacity = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
 
    # Relationships
    manager = relationship("User", foreign_keys=[manager_id])
    teachers = relationship("Teacher", back_populates="center", foreign_keys="[Teacher.center_id]")
    students = relationship("Student", back_populates="center", foreign_keys="[Student.center_id]")
    mosques = relationship("Mosque", back_populates="center")
