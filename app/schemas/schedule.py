from pydantic import BaseModel, Field
from typing import Optional
from datetime import time
from enum import Enum


class DayOfWeek(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class ScheduleBase(BaseModel):
    """Base schema for Schedule"""
    circle_id: int
    day_of_week: DayOfWeek
    start_time: time
    end_time: time
    location: Optional[str] = None
    notes: Optional[str] = None


class ScheduleCreate(ScheduleBase):
    """Schema for creating a new schedule record"""
    pass


class ScheduleUpdate(BaseModel):
    """Schema for updating an existing schedule record"""
    day_of_week: Optional[DayOfWeek] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class Schedule(ScheduleBase):
    """Schema for schedule information returned to clients"""
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True
