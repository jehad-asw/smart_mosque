from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class CenterStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    under_maintenance = "under_maintenance"


class CenterBase(BaseModel):
    """Base schema for Center"""
    name: str
    address: Optional[str] = None
    status: CenterStatus = CenterStatus.active
    phone: Optional[str] = None
    email: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None


class CenterCreate(CenterBase):
    """Schema for creating a new center"""
    manager_id: int


class CenterUpdate(BaseModel):
    """Schema for updating an existing center"""
    name: Optional[str] = None
    address: Optional[str] = None
    status: Optional[CenterStatus] = None
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None


class Center(CenterBase):
    """Schema for center information returned to clients"""
    id: int
    manager_id: int
    
    # Include relationships
    teachers: Optional[List[dict]] = None
    students: Optional[List[dict]] = None
    study_circles: Optional[List[dict]] = None
    
    class Config:
        orm_mode = True
        populate_by_name = True
