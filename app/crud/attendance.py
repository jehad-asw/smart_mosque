from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.attendance import Attendance
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate


def create_attendance(db: Session, attendance: AttendanceCreate) -> Attendance:
    """Create a new attendance record"""
    db_attendance = Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


def get_attendance_by_id(db: Session, attendance_id: int) -> Optional[Attendance]:
    """Get an attendance record by its ID"""
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()


def get_attendance_records(db: Session, skip: int = 0, limit: int = 100) -> List[Attendance]:
    """Get all attendance records with pagination"""
    return db.query(Attendance).offset(skip).limit(limit).all()


def update_attendance(db: Session, attendance_id: int, updates: dict) -> Optional[Attendance]:
    """Update an attendance record"""
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        return None

    for key, value in updates.items():
        setattr(attendance, key, value)

    db.commit()
    db.refresh(attendance)
    return attendance


def delete_attendance(db: Session, attendance_id: int) -> bool:
    """Delete an attendance record by its ID"""
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        return False

    db.delete(attendance)
    db.commit()
    return True