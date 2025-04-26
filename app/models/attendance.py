from sqlalchemy import Column, Integer, ForeignKey, String, Date, Boolean, Enum
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum
from datetime import datetime


class AttendanceStatus(str, enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"


class Attendance(Base):
    """Model for tracking student attendance in study circles"""
    __tablename__ = "attendances"
    
    id = Column(Integer, primary_key=True, index=True)
    circle_id = Column(Integer, ForeignKey("study_circles.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date, default=datetime.utcnow)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.present)
    notes = Column(String, nullable=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    study_circle = relationship("StudyCircle", back_populates="attendance_records")
    student = relationship("Student", back_populates="attendances")
