from fastapi import FastAPI

from app.api.v1.projects import router as projects_router
from app.api.v1.auth import router as auth_router

app = FastAPI(
    title="Genesis AI",
    description="AI Media Factory Backend",
    version="1.0.0",
)

app.include_router(projects_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "project": "Genesis AI",
        "status": "running",
        "message": "Welcome to Genesis 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
