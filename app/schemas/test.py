from pydantic import BaseModel
from datetime import date

class TestBase(BaseModel):
    student_id: int
    tester_id: int
    date: date
    result: str
    level: str

class TestCreate(TestBase):
    pass

class TestUpdate(TestBase):
    pass

class TestResponse(TestBase):
    id: int

    class Config:
        orm_mode = True