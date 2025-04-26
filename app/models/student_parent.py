from sqlalchemy import Column, Integer, ForeignKey, String, Table
from sqlalchemy.orm import relationship
from app.config.database import Base
from datetime import datetime


class StudentParent(Base):
    """Association model for the many-to-many relationship between students and parents"""
    __tablename__ = "student_parents"
    
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), primary_key=True)
    relationship_type = Column(String, nullable=True)  # e.g., "father", "mother", "guardian"
    is_primary_contact = Column(String, default=False)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    
    # Relationships
    student = relationship("Student", back_populates="student_parents")
    parent = relationship("Parent", back_populates="students")
