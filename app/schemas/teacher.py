from pydantic import BaseModel, Field, validator
from typing import Optional, List
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserInDBBase


class TeacherBase(BaseModel):
    """Base schema for Teacher-specific fields"""
    qualifications: Optional[str] = None
    center_id: Optional[int] = None
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    certifications: Optional[str] = None
    availability: Optional[str] = None


class TeacherCreate(UserCreate):
    """Schema for creating a new teacher (includes User fields)"""
    # Teacher-specific fields
    qualifications: Optional[str] = None
    center_id: Optional[int] = None
    specialization: Optional[str] = None
    years_of_experience: Optional[int] = None
    certifications: Optional[str] = None
    availability: Optional[str] = None


class TeacherUpdate(UserUpdate, TeacherBase):
    """Schema for updating an existing teacher"""
    pass


class Teacher(UserInDBBase, TeacherBase):
    """Schema for teacher information returned to clients"""
    # Include relationships
    study_circles: Optional[List[dict]] = None
    
    class Config:
        orm_mode = True

    class Config:
        from_attributes = True
        populate_by_name = True
