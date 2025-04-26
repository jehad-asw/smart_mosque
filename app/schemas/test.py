from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class TestStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"
    pending = "pending"


class TestType(str, Enum):
    written = "written"
    oral = "oral"
    practical = "practical"
    comprehensive = "comprehensive"


class TestBase(BaseModel):
    """Base schema for Test"""
    student_id: int
    examiner_id: int
    test_date: date
    test_type: TestType = TestType.oral
    status: TestStatus = TestStatus.scheduled
    score: Optional[float] = None
    max_score: float = 100.0
    subject: Optional[str] = None
    notes: Optional[str] = None


class TestCreate(TestBase):
    """Schema for creating a new test record"""
    pass


class TestUpdate(BaseModel):
    """Schema for updating an existing test record"""
    test_date: Optional[date] = None
    test_type: Optional[TestType] = None
    status: Optional[TestStatus] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    subject: Optional[str] = None
    notes: Optional[str] = None


class Test(TestBase):
    """Schema for test information returned to clients"""
    id: int
    created_at: str
    updated_at: str
    
    class Config:
        orm_mode = True
