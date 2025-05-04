from sqlalchemy import Column, Integer, String, Enum
from app.config.database import Base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime


class Role(str, enum.Enum):
    admin = "admin"
    subAdmin = "sub-admin"
    teacher = "teacher"
    student = "student"
    staff = "staff"
    parent = "parent"


class NotificationPreference(str, enum.Enum):
    email = "email"
    sms = "sms"
    in_app = "in-app"
    all = "all"


class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"


class User(Base):
    """Base User model that all user types inherit from"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.teacher)
    firstname = Column(String)
    lastname = Column(String)
    phone_number = Column(String)
    address = Column(String)
    status = Column(Enum(UserStatus), default=UserStatus.active)
    notification_preference = Column(Enum(NotificationPreference), default=NotificationPreference.email)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, default=lambda: datetime.utcnow().isoformat(), onupdate=lambda: datetime.utcnow().isoformat())

  # This will be used to determine the type of user in polymorphic queries
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'user'
    }
