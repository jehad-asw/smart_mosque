from pydantic import BaseModel


class StudentBase(BaseModel):
    class_name: str


class StudentCreate(StudentBase):
    pass


class StudentRead(StudentBase):
    id: int
    user_id: int

    class Config:
        orm_moe = True
