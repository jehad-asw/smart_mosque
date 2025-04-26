from app.config.database import engine, Base
from app.models import user, teacher, student  # import all models here

# Create all tables in the database
Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
