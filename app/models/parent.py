from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.models.user import User
from datetime import datetime


class Parent(User):
    """Parent model that inherits from User"""
    __tablename__ = "parents"
    
    # Link to parent User table
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    
    # Parent-specific fields
    occupation = Column(String, nullable=True)
    relationship_to_student = Column(String, nullable=True)  # e.g., father, mother, guardian
    emergency_contact = Column(String, nullable=True)
    preferred_contact_time = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    students = relationship("StudentParent", back_populates="parent")
    
    __mapper_args__ = {
        'polymorphic_identity': 'parent',
    }
