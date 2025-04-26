from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class CircleStudentBase(BaseModel):
    """Base schema for CircleStudent association"""
    circle_id: int
    student_id: int
    join_date: Optional[date] = None
    status: str = "active"
    notes: Optional[str] = None


class CircleStudentCreate(CircleStudentBase):
    """Schema for creating a new circle-student association"""
    pass


class CircleStudentUpdate(BaseModel):
    """Schema for updating an existing circle-student association"""
    status: Optional[str] = None
    notes: Optional[str] = None


class CircleStudent(CircleStudentBase):
    """Schema for circle-student association information returned to clients"""
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True
