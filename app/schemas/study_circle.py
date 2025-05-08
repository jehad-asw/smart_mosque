from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from app.models.study_circle import CircleType, CircleStatus


class StudyCircleBase(BaseModel):
    name: str
    type: Optional[CircleType] = CircleType.group
    teacher_id: int
    center_id: int
    max_capacity: Optional[int] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[CircleStatus] = CircleStatus.active


class StudyCircleCreate(StudyCircleBase):
    pass


class StudyCircleUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[CircleType] = None
    teacher_id: Optional[int] = None
    center_id: Optional[int] = None
    max_capacity: Optional[int] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[CircleStatus] = None


class StudyCircle(StudyCircleBase):
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
