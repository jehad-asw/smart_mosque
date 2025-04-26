from sqlalchemy import Column, Integer, ForeignKey, String, Date, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime


class CircleStudent(Base):
    """Association model for the many-to-many relationship between study circles and students"""
    __tablename__ = "circle_students"
    
    id = Column(Integer, primary_key=True, index=True)
    circle_id = Column(Integer, ForeignKey("study_circles.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    join_date = Column(Date, default=datetime.utcnow)
    status = Column(String, default="active")  # active, inactive, graduated
    notes = Column(String, nullable=True)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    study_circle = relationship("StudyCircle", back_populates="students")
    student = relationship("Student", back_populates="student_circles")
