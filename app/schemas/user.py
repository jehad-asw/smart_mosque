from pydantic import BaseModel, EmailStr
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    subAdmin = "aub-admin"
    teacher = "teacher"
    student = "student"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role = Role.teacher
    firstname: str
    lastname: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role
    firstname: str
    lastname: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
