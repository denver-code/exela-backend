from fastapi import (
    APIRouter,
    Request
)
from app.core.errors.access_denied import access_denied
from app.core.errors.user_exist_error import user_exist_error
from app.core.errors.user_not_exist import user_does_not_exist_error
from app.core.internal.database import delete_one, find, find_one, update_one
from app.core.internal.fast_jwt import FastJWT
from app.core.schemas.event_schemas import EventSchema
from app.core.models.event_model import EventModel


management = APIRouter()


@management.post("/")
async def create_event(_event: EventSchema, request: Request):
    _event = _event.dict()
    
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)
    
    _event["creator"] = int(_user["_id"])
    event = await EventModel().parse_obj(_event).create()

    return event


@management.get("/")
async def get_events_list():
    events = await find("events_db", {})

    return events


@management.get("/{event_id}/")
async def get_event_by_id(event_id: int):
    event = await find_one("events_db", {"_id": event_id})
    if event:
        return event
    return await user_does_not_exist_error("Sorry, event does not exist.")


@management.delete("/{event_id}/")
async def delete_event_by_id(event_id: int, request: Request):
    event = await find_one("events_db", {"_id": event_id})

    if not event:
        return await user_does_not_exist_error("Sorry, event does not exist.")

    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    if _user["_id"] != event["creator"]:
        return await access_denied()

    await delete_one("events_db", {"_id": event_id})

    return {"message": "Success."}


@management.get("/{event_id}/join")
async def join_to_event(event_id: int, request: Request):
    event = await find_one("events_db", {"_id": event_id})

    if not event:
        return await user_does_not_exist_error("Sorry, event does not exist.")

    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    if _user["_id"] in event["participants"]:
        return await user_exist_error("Sorry, user already in event.")
    
    event["participants"].append(_user["_id"])
    await update_one("events_db", {"_id": event_id}, event)

    return {"message": "Success."}


@management.get("/{event_id}/leave")
async def leave_from_event(event_id: int, request: Request):
    event = await find_one("events_db", {"_id": event_id})

    if not event:
        return await user_does_not_exist_error("Sorry, event does not exist.")

    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    if _user["_id"] not in event["participants"]:
        return await user_exist_error("Sorry, user does not joined to event.")
    
    event["participants"].remove(_user["_id"])
    await update_one("events_db", {"_id": event_id}, event)

    return {"message": "Success."}


@management.get("/my")
async def my_event_list(request: Request):
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    events = await find("events_db", {"participants": _user["_id"]})
    
    return events