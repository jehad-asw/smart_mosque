from fastapi import FastAPI

from app.api import auth, teachers, students

app = FastAPI()

app.include_router(auth.router, tags=["Users"])

app.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
#app.include_router(students.router, prefix="/students", tags=["Students"])
