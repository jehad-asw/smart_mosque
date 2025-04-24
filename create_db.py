from app.config.database import engine, Base
from app.models import user, teacher, student  # import all models here

Base.metadata.create_all(bind=engine)
