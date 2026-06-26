from fastapi import FastAPI

app = FastAPI(
    title="Genesis AI",
    description="AI Media Factory Backend",
    version="1.0.0"
)


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