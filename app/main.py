from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware

from app.api import auth, teachers, students, parents, centers, attendance, mosques, study_circle



app = FastAPI(
    title="Smart Mosque API",
    description="API for Smart Mosque Educational Management System",
    version="1.0.0",
    openapi_tags=[
        {"name": "Authentication", "description": "Operations with authentication"},
        {"name": "Teachers", "description": "Operations with teachers"},
        {"name": "Students", "description": "Operations with students"},
        {"name": "Parents", "description": "Operations with parents"},
        {"name": "Centers", "description": "Operations with centers"},
        {"name": "Mosques", "description": "Operations with mosques"},
        {"name": "Attendance", "description": "Operations with attendance"},
        {"name": "Study Circles", "description": "Operations with study circles"}
    ]
)

# Define OAuth2 scheme for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Configure security for all endpoints
app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True
}

# Add middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(LoggingMiddleware)

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
app.include_router(centers.router, prefix="/centers", tags=["Centers"])
app.include_router(mosques.router, prefix="/mosques", tags=["Mosques"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(study_circle.router, prefix="/study-circles", tags=["Study Circles"])


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint that returns API information"""
    return {
        "name": "Smart Mosque API",
        "version": "1.0.0",
        "description": "API for Smart Mosque Educational Management System"
    }
