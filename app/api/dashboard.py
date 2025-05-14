from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.deps.db import get_db
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.study_circle import StudyCircle
from app.models.center import Center
from app.models.mosque import Mosque
from app.services.dashboard_service import get_dashboard_data

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Return detailed dashboard stats per center, including mosques and study circles."""
    return get_dashboard_data(db)
