from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import date
from enum import Enum
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserInDBBase


class ExemptionStatus(str, Enum):
    exempted = "exempted"
    non_exempted = "non-exempted"
    partial = "partial"


class Gender(str, Enum):
    male = "male"
    female = "female"


class StudentBase(BaseModel):
    """Base schema for Student-specific fields"""
    level: Optional[str] = None
    exemption_status: ExemptionStatus = ExemptionStatus.non_exempted
    center_id: Optional[int] = None
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    nationality: Optional[str] = None
    id_number: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_conditions: Optional[str] = None
    registration_date: Optional[date] = None
    preferred_circle_id: Optional[int] = None
    previous_education: Optional[str] = None


class StudentCreate(UserCreate):
    """Schema for creating a new student (includes User fields)"""
    # Student-specific fields
    level: str
    exemption_status: ExemptionStatus = ExemptionStatus.non_exempted
    center_id: Optional[int] = None
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    nationality: Optional[str] = None
    id_number: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    emergency_contact: Optional[str] = None
    medical_conditions: Optional[str] = None
    registration_date: Optional[date] = None
    preferred_circle_id: Optional[int] = None
    previous_education: Optional[str] = None


class StudentUpdate(UserUpdate, StudentBase):
    """Schema for updating an existing student"""
    pass


class Student(UserInDBBase, StudentBase):
    """Schema for student information returned to clients"""
    # Include relationships
    student_circles: Optional[List[dict]] = None
    attendances: Optional[List[dict]] = None
    tests: Optional[List[dict]] = None
    student_parents: Optional[List[dict]] = None
    
    class Config:
        orm_mode = True


class StudentRead(StudentBase):
    id: int
    user_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True
