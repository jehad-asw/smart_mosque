from sqlalchemy.orm import Session
from app.models.center import Center
from app.schemas.center import CenterCreate, CenterUpdate

def get_center(db: Session, center_id: int):
    return db.query(Center).filter(Center.id == center_id).first()

def get_centers(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Center).offset(skip).limit(limit).all()

def create_center(db: Session, center: CenterCreate):
    db_center = Center(**center.dict())
    db.add(db_center)
    db.commit()
    db.refresh(db_center)
    return db_center

def update_center(db: Session, center_id: int, center: CenterUpdate):
    db_center = db.query(Center).filter(Center.id == center_id).first()
    if not db_center:
        return None
    for key, value in center.dict(exclude_unset=True).items():
        setattr(db_center, key, value)
    db.commit()
    db.refresh(db_center)
    return db_center

def delete_center(db: Session, center_id: int):
    db_center = db.query(Center).filter(Center.id == center_id).first()
    if db_center:
        db.delete(db_center)
        db.commit()
    return db_center