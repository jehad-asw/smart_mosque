from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.teacher import TeacherCreate, Teacher, TeacherUpdate
from app.crud import user as user_crud
from app.models.user import Role
from app.deps.db import get_db, get_current_user, require_role


router = APIRouter()


@router.get("/", response_model=List[Teacher])
def get_teachers(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Get a list of all teachers"""
    return user_crud.get_users_by_role(db, Role.teacher, skip, limit)


@router.get("/me", response_model=Teacher)
def get_teacher_profile(current_user=Depends(require_role(Role.teacher))):
    """Get the current teacher's profile"""

    return current_user
