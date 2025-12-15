import json
import threading
import time
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import FastAPI,APIRouter

from app.core.database import get_db
from sqlalchemy import text
from app.api.route_main import api_router
from app.api.routes.user_payload import generate_user_payloa
from app.core.database import init_db
from app.core.redis_config import (
    cache_permissions,
    cache_user_dept_gpt_store_mapping,
    cache_user_id_with_roles,
    connect_redis,
)
print("test")



app = FastAPI(
    lifespan=lifespan,
    root_path="/dashboard",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


# @app.get("/")
# async def root():
#     return {"message": "This is the demo Root endpoint"}

@app.get("/")
async def root(db: Session = Depends(get_db)):
    db_status = "skipped"
    if os.getenv("SQLALCHEMY_DATABASE_URL"):
        try:
            db.execute(text("SELECT 1"))
            db_status = "connected"
        except SQLAlchemyError:
            db_status = "unreachable"

    return {
        "message": "This is the demo Root endpoint",
        "db": db_status
    }





