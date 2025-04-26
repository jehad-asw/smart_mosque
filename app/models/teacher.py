from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.models.user import User
from datetime import datetime


class Teacher(User):
    """Teacher model that inherits from User"""
    __tablename__ = "teachers"
    
    # Link to parent User table
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    # Teacher-specific fields
    qualifications = Column(Text, nullable=True)
    center_id = Column(Integer, ForeignKey("centers.id"), nullable=True)
    specialization = Column(String, nullable=True)
    years_of_experience = Column(Integer, nullable=True)
    certifications = Column(Text, nullable=True)
    availability = Column(String, nullable=True)  # Could be JSON string with schedule information
    
    # Relationships
    center = relationship("Center", back_populates="teachers")
    study_circles = relationship("StudyCircle", back_populates="teacher")
    
    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }
