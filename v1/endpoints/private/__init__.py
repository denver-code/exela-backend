from fastapi import (
    APIRouter,
    Depends
)

from app.core.middlewares.login_required import login_required
from v1.endpoints.private.user import user
from v1.endpoints.private.event import event
from v1.endpoints.private.group import group
from v1.endpoints.private.messaging import messaging

private = APIRouter(prefix="/private", dependencies=[Depends(login_required)])

private.include_router(user)
private.include_router(event)
private.include_router(group)
private.include_router(messaging)

@private.get("/", dependencies=[])
async def protected_showcase():
    return {"message":"Great! You on protected page!"}