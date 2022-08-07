from datetime import datetime
from fastapi import (
    APIRouter
)
from v1.endpoints.private import private
from v1.endpoints.public import public 

v1 = APIRouter(prefix="/api/v1")


@v1.get("/")
async def showcase_event():
    return {
        "name": "Exela.inc backend",
        "version": "v1 0.1.0",
        "python": "3.10.5",
        "fastapi": "0.68.0",
        "docs": "/api/v1/docs",
        "server_time": datetime.today()
    }

v1.include_router(public)
v1.include_router(private)