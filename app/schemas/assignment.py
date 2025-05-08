from pydantic import BaseModel
from datetime import date

class AssignmentBase(BaseModel):
    student_id: int
    tester_id: int
    date: date
    result: str
    level: str

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    id: int

    class Config:
        orm_mode = True