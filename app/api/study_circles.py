from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.study_circle import StudyCircleCreate, StudyCircleUpdate, StudyCircle
from app.services.study_circle import (
    create_study_circle,
    get_study_circle_by_id,
    get_all_study_circles,
    update_study_circle,
    delete_study_circle,
)
from app.deps.db import get_db

router = APIRouter()


@router.post("/", response_model=StudyCircle)
def create_new_study_circle(study_circle: StudyCircleCreate, db: Session = Depends(get_db)):
    return create_study_circle(db, study_circle)


@router.get("/{id}", response_model=StudyCircle)
def get_study_circle(id: int, db: Session = Depends(get_db)):
    study_circle = get_study_circle_by_id(db, id)
    if not study_circle:
        raise HTTPException(status_code=404, detail="Study circle not found")
    return study_circle


@router.get("/", response_model=List[StudyCircle])
def get_all_study_circles_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_all_study_circles(db, skip=skip, limit=limit)


@router.put("/{id}", response_model=StudyCircle)
def update_existing_study_circle(id: int, study_circle: StudyCircleUpdate, db: Session = Depends(get_db)):
    updated_circle = update_study_circle(db, id, study_circle.dict(exclude_unset=True))
    if not updated_circle:
        raise HTTPException(status_code=404, detail="Study circle not found")
    return updated_circle


@router.delete("/{id}", response_model=dict)
def delete_existing_study_circle(id: int, db: Session = Depends(get_db)):
    success = delete_study_circle(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Study circle not found")
    return {"detail": "Study circle deleted successfully"}