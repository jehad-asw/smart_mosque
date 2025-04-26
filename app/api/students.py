from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.student import StudentCreate, Student, StudentUpdate
from app.crud import user as user_crud
from app.models.user import Role
from app.deps.db import get_db, get_current_user


router = APIRouter()


@router.get("/", response_model=List[Student])
def get_students(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Get a list of all students"""
    return user_crud.get_users_by_role(db, Role.student, skip, limit)


@router.get("/me", response_model=Student)
def get_student_profile(current_user=Depends(get_current_user)):
    """Get the current student's profile"""
    if current_user.role != Role.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a student"
        )
    return current_user
