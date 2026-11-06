from fastapi import FastAPI

from app.database.database import Base, engine
from app import models

import asyncio

from app.database.database import SessionLocal
from app.services.request_expiry import expire_pending_requests

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

from app.routers.access_log import router as access_log_router

app.include_router(access_log_router)



async def request_expiry_scheduler():
    while True:
        db = SessionLocal()

        try:
            count = expire_pending_requests(db)

            if count > 0:
                print(f"Expired {count} access request(s)")

        except Exception as e:
            print(f"Request expiry scheduler error: {e}")

        finally:
            db.close()

        await asyncio.sleep(10)

        expiry_task = None


@app.on_event("startup")
async def start_expiry_scheduler():
    global expiry_task
    expiry_task = asyncio.create_task(
        request_expiry_scheduler()
    )


@app.on_event("shutdown")
async def stop_expiry_scheduler():
    global expiry_task

    if expiry_task:
        expiry_task.cancel()

        try:
            await expiry_task
        except asyncio.CancelledError:
            pass