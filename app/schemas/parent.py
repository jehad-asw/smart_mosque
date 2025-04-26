from pydantic import BaseModel, Field, validator
from typing import Optional, List
from app.schemas.user import UserBase, UserCreate, UserUpdate, UserInDBBase


class ParentBase(BaseModel):
    """Base schema for Parent-specific fields"""
    occupation: Optional[str] = None
    relationship_to_student: Optional[str] = None
    emergency_contact: Optional[str] = None
    preferred_contact_time: Optional[str] = None
    notes: Optional[str] = None


class ParentCreate(UserCreate):
    """Schema for creating a new parent (includes User fields)"""
    # Parent-specific fields
    occupation: Optional[str] = None
    relationship_to_student: Optional[str] = None
    emergency_contact: Optional[str] = None
    preferred_contact_time: Optional[str] = None
    notes: Optional[str] = None


class ParentUpdate(UserUpdate, ParentBase):
    """Schema for updating an existing parent"""
    pass


class Parent(UserInDBBase, ParentBase):
    """Schema for parent information returned to clients"""
    # Include relationships
    students: Optional[List[dict]] = None
    
    class Config:
        orm_mode = True
