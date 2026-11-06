from fastapi import FastAPI

app = FastAPI(
    title="SmartCabin API",
    description="Cabin Security Management System",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SmartCabin API",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}