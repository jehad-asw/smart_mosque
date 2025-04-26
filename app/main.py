from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, teachers, students, parents

app = FastAPI(
    title="Smart Mosque API",
    description="API for Smart Mosque Educational Management System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# User type specific routes
app.include_router(teachers.router, prefix="/teachers", tags=["Teachers"])
app.include_router(students.router, prefix="/students", tags=["Students"])
app.include_router(parents.router, prefix="/parents", tags=["Parents"])


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint that returns API information"""
    return {
        "name": "Smart Mosque API",
        "version": "1.0.0",
        "description": "API for Smart Mosque Educational Management System"
    }
