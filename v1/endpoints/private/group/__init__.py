from fastapi import(
    APIRouter
)
from v1.endpoints.private.group.management import management


group = APIRouter(prefix="/group")

group.include_router(management)
