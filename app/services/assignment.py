from sqlalchemy.orm import Session
from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate

def create_assignment(db: Session, assignment: AssignmentCreate) -> Assignment:
    db_assignment = Assignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def update_assignment(db: Session, id: int, assignment: AssignmentUpdate) -> Assignment:
    db_assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if not db_assignment:
        return None
    for key, value in assignment.dict().items():
        setattr(db_assignment, key, value)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

def delete_assignment(db: Session, id: int):
    db_assignment = db.query(Assignment).filter(Assignment.id == id).first()
    if db_assignment:
        db.delete(db_assignment)
        db.commit()

def get_all_assignments(db: Session):
    return db.query(Assignment).all()

def get_assignment_by_id(db: Session, id: int) -> Assignment:
    return db.query(Assignment).filter(Assignment.id == id).first()