from fastapi import FastAPI

from app.database.database import Base, engine
from app import models



Base.metadata.create_all(bind=engine)

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

from app.routers.owner import router as owner_router

app.include_router(owner_router)

from app.routers.auth import router as auth_router

app.include_router(auth_router)

from app.routers.admin import router as admin_router

app.include_router(admin_router)

from app.routers.visitor import router as visitor_router

app.include_router(visitor_router)


from app.routers.device import router as device_router

app.include_router(device_router)

from app.routers.access_request import router as access_request_router

app.include_router(access_request_router)