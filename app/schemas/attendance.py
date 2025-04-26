from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"


class AttendanceBase(BaseModel):
    """Base schema for Attendance"""
    circle_id: int
    student_id: int
    date: date
    status: AttendanceStatus = AttendanceStatus.present
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    """Schema for creating a new attendance record"""
    pass


class AttendanceUpdate(BaseModel):
    """Schema for updating an existing attendance record"""
    status: Optional[AttendanceStatus] = None
    notes: Optional[str] = None


class Attendance(AttendanceBase):
    """Schema for attendance information returned to clients"""
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True
