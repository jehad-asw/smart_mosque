from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.teacher import TeacherCreate, TeacherRead
from app.crud import teacher as teacher_crud
from app.deps.db import get_db, get_current_user


router = APIRouter()


@router.post("/", response_model=TeacherRead)
def register_teacher(teacher_in: TeacherCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return teacher_crud.create_teacher(db=db, user_id=user.id, teacher=teacher_in)


@router.get("/me", response_model=TeacherRead)
def get_teacher_profile(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return teacher_crud.get_teacher_by_user(db=db, user_id=user.id)
