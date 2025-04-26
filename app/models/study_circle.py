from sqlalchemy import Column, Integer, ForeignKey, String, Enum, Text, Date
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum
from datetime import datetime


class CircleType(str, enum.Enum):
    individual = "individual"
    group = "group"


class CircleStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    completed = "completed"
    cancelled = "cancelled"


class StudyCircle(Base):
    """Model for managing study circles"""
    __tablename__ = "study_circles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(CircleType), default=CircleType.group)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    center_id = Column(Integer, ForeignKey("centers.id"))
    max_capacity = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(Enum(CircleStatus), default=CircleStatus.active)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())

    # Relationships
    teacher = relationship("Teacher", back_populates="study_circles")
    center = relationship("Center", back_populates="study_circles")
    students = relationship("CircleStudent", back_populates="study_circle")
    attendance_records = relationship("Attendance", back_populates="study_circle")
    schedules = relationship("Schedule", back_populates="study_circle")
