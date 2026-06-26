from app.db.database import engine
from app.models.project import Project
from app.db.database import Base

Base.metadata.create_all(bind=engine)

print("Database initialized successfully!")