from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.teacher import TeacherCreate, Teacher, TeacherUpdate
from app.services import user as user_crud
from app.services import teacher as teacher_crud
from app.models.user import Role
from app.deps.db import get_db, get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# get all teachers
@router.get("/", response_model=List[Teacher])
def get_teachers(
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
    skip: int = 0, 
    limit: int = 100
):
    """Get a list of all teachers"""
    return user_crud.get_users_by_role(db, Role.teacher, skip, limit)

# return teacher information
@router.get("/me", response_model=Teacher)
def get_teacher_profile(
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Get the current teacher's profile"""
    if current_user.role != Role.teacher:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a teacher"
        )
    return current_user

# get teacher by id
@router.get("/{id}", response_model=Teacher)
async def get_teacher_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Get a teacher by ID"""
    teacher = teacher_crud.get_teacher_by_id(db, id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

# get teachers by center name
@router.get("/by-center/{center_name}", response_model=List[Teacher])
def get_teachers_by_center_name(center_name: str, db: Session = Depends(get_db)):
    """Get a list of teachers by center name"""
    teachers = teacher_crud.get_teachers_by_center_name(db, center_name)
    if not teachers:
        raise HTTPException(status_code=404, detail="No teachers found for this center")
    return teachers

# modify teacher information
@router.put("/teachers/{id}", response_model=Teacher)
def update_existing_teacher(id: int, teacher: TeacherUpdate, db: Session = Depends(get_db)):
    db_teacher = teacher_crud.update_teacher(db, id, teacher)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="teacher not found")
    return db_teacher

# delete teacher
@router.delete("/teachers/{id}", response_model=Teacher)
def delete_existing_teacher(id: int, db: Session = Depends(get_db)):
    db_teacher = teacher_crud.delete_teacher(db, id)
    if not db_teacher:
        raise HTTPException(status_code=404, detail="teacher not found")
    return db_teacher

