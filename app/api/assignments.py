from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentResponse
from app.crud.assignment import create_assignment, update_assignment, delete_assignment, get_all_assignments, get_assignment_by_id
from app.deps.db import get_db

router = APIRouter()

@router.post("/assignments", response_model=AssignmentResponse)
def create_assignment_endpoint(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    return create_assignment(db, assignment)

@router.put("/assignments/{id}", response_model=AssignmentResponse)
def update_assignment_endpoint(id: int, assignment: AssignmentUpdate, db: Session = Depends(get_db)):
    db_assignment = get_assignment_by_id(db, id)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return update_assignment(db, id, assignment)

@router.delete("/assignments/{id}")
def delete_assignment_endpoint(id: int, db: Session = Depends(get_db)):
    db_assignment = get_assignment_by_id(db, id)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    delete_assignment(db, id)
    return {"message": "Assignment deleted successfully"}

@router.get("/assignments", response_model=list[AssignmentResponse])
def get_all_assignments_endpoint(db: Session = Depends(get_db)):
    return get_all_assignments(db)

@router.get("/assignments/{id}", response_model=AssignmentResponse)
def get_assignment_by_id_endpoint(id: int, db: Session = Depends(get_db)):
    db_assignment = get_assignment_by_id(db, id)
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return db_assignment