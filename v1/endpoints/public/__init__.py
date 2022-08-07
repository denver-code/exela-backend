from fastapi import (
    APIRouter
)

from v1.endpoints.public.authorization import authorization

public = APIRouter(prefix="/public")

public.include_router(authorization)