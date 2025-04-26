from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import date


class CircleType(str, Enum):
    individual = "individual"
    group = "group"


class CircleStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    completed = "completed"
    cancelled = "cancelled"


class CircleBase(BaseModel):
    """Base schema for Study Circle"""
    name: str
    type: CircleType = CircleType.group
    teacher_id: int
    center_id: int
    max_capacity: Optional[int] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: CircleStatus = CircleStatus.active


class CircleCreate(CircleBase):
    """Schema for creating a new study circle"""
    pass


class CircleUpdate(BaseModel):
    """Schema for updating an existing study circle"""
    name: Optional[str] = None
    type: Optional[CircleType] = None
    teacher_id: Optional[int] = None
    center_id: Optional[int] = None
    max_capacity: Optional[int] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[CircleStatus] = None


class Circle(CircleBase):
    """Schema for study circle information returned to clients"""
    id: int
    created_at: str
    updated_at: str
    
    # Include relationships
    teacher: Optional[dict] = None
    center: Optional[dict] = None
    students: Optional[List[dict]] = None
    attendance_records: Optional[List[dict]] = None
    schedules: Optional[List[dict]] = None
    
    class Config:
        orm_mode = True
        populate_by_name = True
