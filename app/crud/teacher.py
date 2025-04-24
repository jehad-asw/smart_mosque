from sqlalchemy.orm import Session
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate


def create_teacher(db: Session, user_id: int, teacher: TeacherCreate):
    db_teacher = Teacher(**teacher.dict(), user_id=user_id)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher


def get_teacher_by_user(db: Session, user_id: int):
    return db.query(Teacher).filter(Teacher.user_id == user_id).first()
