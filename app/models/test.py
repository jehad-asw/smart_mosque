from sqlalchemy import Column, Integer, ForeignKey, String, Date, Float, Enum, Text
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum
from datetime import datetime


class TestStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"
    pending = "pending"


class TestType(str, enum.Enum):
    written = "written"
    oral = "oral"
    practical = "practical"
    comprehensive = "comprehensive"


class Test(Base):
    """Model for tracking student tests and evaluations"""
    __tablename__ = "tests"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    examiner_id = Column(Integer, ForeignKey("users.id"))
    test_date = Column(Date, default=datetime.utcnow)
    test_type = Column(Enum(TestType), default=TestType.oral)
    status = Column(Enum(TestStatus), default=TestStatus.scheduled)
    score = Column(Float, nullable=True)
    max_score = Column(Float, default=100.0)
    subject = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    student = relationship("Student", back_populates="tests", foreign_keys=[student_id])
    examiner = relationship("User", foreign_keys=[examiner_id])
