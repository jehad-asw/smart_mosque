from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StudentParentBase(BaseModel):
    """Base schema for StudentParent association"""
    student_id: int
    parent_id: int
    relationship_type: Optional[str] = None
    is_primary_contact: bool = False


class StudentParentCreate(StudentParentBase):
    """Schema for creating a new student-parent association"""
    pass


class StudentParentUpdate(BaseModel):
    """Schema for updating an existing student-parent association"""
    relationship_type: Optional[str] = None
    is_primary_contact: Optional[bool] = None


class StudentParent(StudentParentBase):
    """Schema for student-parent association information returned to clients"""
    created_at: str
    
    class Config:
        orm_mode = True
