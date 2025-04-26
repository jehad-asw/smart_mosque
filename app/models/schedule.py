from sqlalchemy import Column, Integer, ForeignKey, String, Time, Enum, Text
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum
from datetime import datetime


class DayOfWeek(str, enum.Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class Schedule(Base):
    """Model for tracking study circle schedules"""
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    circle_id = Column(Integer, ForeignKey("study_circles.id"))
    day_of_week = Column(Enum(DayOfWeek))
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    study_circle = relationship("StudyCircle", back_populates="schedules")
