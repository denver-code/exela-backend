from fastapi import(
    APIRouter
)
from v1.endpoints.private.event.management import management


event = APIRouter(prefix="/event")

event.include_router(management)
