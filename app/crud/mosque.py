from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.mosque import Mosque
from app.schemas.mosque import MosqueCreate, MosqueUpdate


def create_mosque(db: Session, mosque: MosqueCreate) -> Mosque:
    """Create a new mosque"""
    db_mosque = Mosque(**mosque.dict())
    db.add(db_mosque)
    db.commit()
    db.refresh(db_mosque)
    return db_mosque


def get_mosque_by_id(db: Session, mosque_id: int) -> Optional[Mosque]:
    """Get a mosque by its ID"""
    return db.query(Mosque).filter(Mosque.id == mosque_id).first()


def get_all_mosques(db: Session, skip: int = 0, limit: int = 100) -> List[Mosque]:
    """Get all mosques with pagination"""
    return db.query(Mosque).offset(skip).limit(limit).all()


def update_mosque(db: Session, mosque_id: int, updates: dict) -> Optional[Mosque]:
    """Update a mosque's details"""
    mosque = db.query(Mosque).filter(Mosque.id == mosque_id).first()
    if not mosque:
        return None

    for key, value in updates.items():
        setattr(mosque, key, value)

    db.commit()
    db.refresh(mosque)
    return mosque


def delete_mosque(db: Session, mosque_id: int) -> bool:
    """Delete a mosque by its ID"""
    mosque = db.query(Mosque).filter(Mosque.id == mosque_id).first()
    if not mosque:
        return False

    db.delete(mosque)
    db.commit()
    return True