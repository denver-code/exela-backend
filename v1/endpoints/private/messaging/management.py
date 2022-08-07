from multiprocessing import managers
from fastapi import (
    APIRouter,
    Request
)
from app.core.errors.access_denied import access_denied
from app.core.errors.user_exist_error import user_exist_error
from app.core.errors.user_not_exist import user_does_not_exist_error
from app.core.internal.database import delete_one, find, find_one

from app.core.internal.fast_jwt import FastJWT
from app.core.models.message_model import MessageModel
from app.core.schemas.message_schemas import MessageSchema


management = APIRouter()


@management.post("/{recipient_type}/{recipient_id}/")
async def new_message_event(recipient_type: str, recipient_id: int, __message: MessageSchema, request: Request):
    _db_name = "groups_db"
    _name = "name"
    if recipient_type == "user":
        _name = "username"
        _db_name = "users_db"
    
    _target = await find_one(_db_name, {"_id": recipient_id})

    if not _target:
        return await user_does_not_exist_error("Sorry, target does not exist.")
    
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    if _db_name == "groups_db":
        if _user["_id"] not in _target["participants"]:
            return await user_exist_error("Sorry, user does not joined to group.")
    
    __message = __message.dict()

    _message = await MessageModel(
        text = __message["text"],
        alias = _db_name[:-4],
        metadata = {
            "sender_name": _user["username"],
            "sender_id": _user["_id"],
            "recipient_name": _target[_name],
            "recipient_id": recipient_id
        },
        recipient = recipient_id,
        sender = _user["_id"]
    ).create(_db="messages_db")

    return _message


@management.get("/{recipient_type}/{recipient_id}/")
async def get_messages_event(recipient_type: str, recipient_id: int, request: Request):
    _db_name = "groups_db"
    if recipient_type == "user":
        _db_name = "users_db"
    
    _target = await find_one(_db_name, {"_id": recipient_id})

    if not _target:
        return await user_does_not_exist_error("Sorry, target does not exist.")
    
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    if _db_name == "groups_db":
        if _user["_id"] not in _target["participants"]:
            return await user_exist_error("Sorry, user does not joined to group.")
    
    messages = await find("messages_db", {
        "alias": recipient_type,
        "recipient":recipient_id
    })

    # idk if we need that right now :)
    # messages.reverse()

    return messages


@management.get("/my")
async def get_my_messages_event(request: Request):
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    messages = await find("messages_db", {
        "sender": _user["_id"]
    })

    # idk if we need that right now :)
    # messages.reverse()

    return messages


@management.delete("/{message_id}")
async def delete_message_event(message_id: int, request: Request):
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)
 
    target = await find_one("messages_db", {"_id":message_id})

    if not target:
        return await user_does_not_exist_error("Sorry, target does not exist.")
    
    if target["sender"] != _user["_id"]:
        return await access_denied()

    await delete_one("messages_db", {"_id": message_id})

    return {"message": "Success."}

    