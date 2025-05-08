from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, String, Date, Boolean, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime
import enum


class CircleStudentStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    graduated = "graduated"

class CircleStudent(Base):
    """Association model for the many-to-many relationship between study circles and students"""
    __tablename__ = "circle_students"
    
    id = Column(Integer, primary_key=True, index=True)
    circle_id = Column(Integer, ForeignKey("study_circles.id"), index=True)
    student_id = Column(Integer, ForeignKey("students.id"),index=True)
    join_date = Column(Date, default=datetime.utcnow)
    status = Column(Enum(CircleStudentStatus), default=CircleStudentStatus.active)
    notes = Column(String, nullable=True)
 
    # Relationships
    study_circle = relationship("StudyCircle", back_populates="students")
    student = relationship("Student", back_populates="student_circles")
