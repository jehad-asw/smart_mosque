from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.study_circle import StudyCircle
from app.schemas.study_circle import StudyCircleCreate, StudyCircleUpdate


def create_study_circle(db: Session, study_circle: StudyCircleCreate) -> StudyCircle:
    """Create a new study circle"""
    db_study_circle = StudyCircle(**study_circle.dict())
    db.add(db_study_circle)
    db.commit()
    db.refresh(db_study_circle)
    return db_study_circle


def get_study_circle_by_id(db: Session, id: int) -> Optional[StudyCircle]:
    """Get a study circle by its ID"""
    return db.query(StudyCircle).filter(StudyCircle.id == id).first()


def get_all_study_circles(db: Session, skip: int = 0, limit: int = 100) -> List[StudyCircle]:
    """Get all study circles with pagination"""
    return db.query(StudyCircle).offset(skip).limit(limit).all()


def update_study_circle(db: Session, id: int, updates: dict) -> Optional[StudyCircle]:
    """Update a study circle"""
    study_circle = db.query(StudyCircle).filter(StudyCircle.id == id).first()
    if not study_circle:
        return None

    for key, value in updates.items():
        setattr(study_circle, key, value)

    db.commit()
    db.refresh(study_circle)
    return study_circle


def delete_study_circle(db: Session, id: int) -> bool:
    """Delete a study circle by its ID"""
    study_circle = db.query(StudyCircle).filter(StudyCircle.id == id).first()
    if not study_circle:
        return False

    db.delete(study_circle)
    db.commit()
    return True