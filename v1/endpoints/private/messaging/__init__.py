from fastapi import(
    APIRouter
)
from v1.endpoints.private.messaging.management import management


messaging = APIRouter(prefix="/message")

messaging.include_router(management)
