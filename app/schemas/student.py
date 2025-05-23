from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from app.schemas.user import UserBase, UserCreate, User, UserUpdate
from app.models.student import ExemptionStatus, Gender

class StudentBase(UserBase):
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
    previous_education: Optional[str] = None

class StudentCreate(UserCreate, StudentBase):
    """Schema for creating a new student"""
    pass

class StudentUpdate(UserUpdate, StudentBase):
    """Schema for updating a student"""
    level: Optional[str] = None
    exemption_status: Optional[ExemptionStatus] = None
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
    previous_education: Optional[str] = None


class Student(User, StudentBase):
    """Schema for student response"""
    pass
