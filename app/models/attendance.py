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

class UserType(str, enum.Enum):
    student = "student"
    teacher = "teacher"

class Attendance(Base):
    """Model for tracking attendance for both students and teachers"""
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)
    circle_id = Column(Integer, ForeignKey("study_circles.id"), nullable=True)  # For students
    mosque_id = Column(Integer, ForeignKey("mosques.id"), nullable=True)  # For teachers
    date = Column(Date, default=datetime.utcnow)
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.present)
    notes = Column(String, nullable=True)

    # Relationships
    student = relationship("Student", back_populates="attendances")
    teacher = relationship("Teacher", back_populates="attendances")
    study_circle = relationship("StudyCircle", back_populates="attendance_records")
    mosque = relationship("Mosque", back_populates="attendance_records")

