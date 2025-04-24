from pydantic import BaseModel


class TeacherBase(BaseModel):
    subject: str


class TeacherCreate(TeacherBase):
    pass


class TeacherRead(TeacherBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
