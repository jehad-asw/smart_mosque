from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from enum import Enum
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date


class Role(str, Enum):
    admin = "admin"
    subAdmin = "sub-admin"
    teacher = "teacher"
    student = "student"
    parent = "parent"
    staff = "staff"


class NotificationPreference(str, Enum):
    email = "email"
    sms = "sms"
    in_app = "in-app"
    all = "all"


class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"


class UserType(str, Enum):
    user = "user"
    teacher = "teacher"
    student = "student"
    parent = "parent"


class UserBase(BaseModel):
    """Base schema for User with common fields"""
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    role: Role
    phone_number: Optional[str] = None
    address: Optional[str] = None
    notification_preference: NotificationPreference = NotificationPreference.email
    status: UserStatus = UserStatus.active

    @field_validator('username')
    def username_must_be_valid(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        return v


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str
    
    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserUpdate(BaseModel):
    """Schema for updating an existing user"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    notification_preference: Optional[NotificationPreference] = None
    status: Optional[UserStatus] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('password')
    def password_must_be_strong(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserInDBBase(UserBase):
    """Schema for user information retrieved from the database"""
    id: int
    created_at: str
    updated_at: str
    type: UserType

    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    """Schema for user information returned to clients"""
    pass


class UserWithPassword(UserInDBBase):
    """Schema that includes the hashed password (for internal use only)"""
    hashed_password: str


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    
    @field_validator('password')
    def password_must_not_be_empty(cls, v):
        if not v or len(v) < 1:
            raise ValueError('Password cannot be empty')
        return v
