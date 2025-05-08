from typing import Optional
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

def get_teacher_by_id(db: Session, teacher_id: int) -> Optional[Teacher]:
    """Get a teacher by their ID"""
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()

def update_teacher(db: Session, teacher_id: int, updates: dict) -> Optional[Teacher]:
    """Update a teacher's details"""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        return None

    for key, value in updates.items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher

def delete_teacher(db: Session, teacher_id: int) -> bool:
    """Delete a teacher by their ID"""
    teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
    if not teacher:
        return False

    db.delete(teacher)
    db.commit()
    return True