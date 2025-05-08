from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, Attendance
from app.crud.attendance import (
    create_attendance,
    get_attendance_by_id,
    get_attendance_records,
    update_attendance,
    delete_attendance,
)
from app.deps.db import get_db

router = APIRouter()


@router.post("/", response_model=Attendance)
def create_new_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    return create_attendance(db, attendance)


@router.get("/{attendance_id}", response_model=Attendance)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    record = get_attendance_by_id(db, attendance_id)
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return record


@router.get("/", response_model=List[Attendance])
def get_all_attendance_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_attendance_records(db, skip=skip, limit=limit)


@router.put("/{attendance_id}", response_model=Attendance)
def update_existing_attendance(attendance_id: int, attendance: AttendanceUpdate, db: Session = Depends(get_db)):
    updated_record = update_attendance(db, attendance_id, attendance.dict(exclude_unset=True))
    if not updated_record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return updated_record


@router.delete("/{attendance_id}", response_model=dict)
def delete_existing_attendance(attendance_id: int, db: Session = Depends(get_db)):
    success = delete_attendance(db, attendance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    return {"detail": "Attendance record deleted successfully"}