from sqlalchemy import Column, Integer, String, Enum
from app.config.database import Base
import enum


class Role(str, enum.Enum):
    admin = "admin",
    subAdmin = "aub-admin"
    teacher = "teacher"
    student = "student"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    role = Column(Enum(Role), default=Role.teacher)
