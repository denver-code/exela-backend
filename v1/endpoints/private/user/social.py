import time
from datetime import datetime

from fastapi import (
    APIRouter,
    Request
)
from app.core.errors.already_friends import already_friends_error
from app.core.errors.request_not_found import request_not_found
from app.core.errors.request_ongoing import request_ongoing
from app.core.errors.self_error import self_error
from app.core.errors.user_not_exist import user_does_not_exist_error

from app.core.internal.fast_jwt import FastJWT
from app.core.internal.database import delete_one, find_one, update_one, insert_many
from app.core.internal.represents_int import represents_int

from app.core.models.friend_request import FriendRequest


social = APIRouter(prefix="/social")


@social.post("/addfriend/{user_id}")
async def add_friend_event(request: Request, user_id):
    auth_header = request.headers.get('Authorization')
    
    _id = (await FastJWT().decode(auth_header))["_id"]

    _user = await find_one("users_db", {"_id": _id})

    _key = "username"

    if await represents_int(user_id):
        user_id = int(user_id)
        _key = "_id"

    user = await find_one("users_db", {_key: user_id})

    if user["_id"] in _user["friends"]:
        return await already_friends_error()

    if _user == user:
        return await self_error()

    if not user:
        return await user_does_not_exist_error()

    today = datetime.now()

    if await find_one("requests_db", {
        "sender": _id,
        "receiver": user["_id"]
    }):
        return await request_ongoing()
 
    _friend_request = FriendRequest(
        request_type="friendship",
        sender=_id,
        receiver=user["_id"],
        metadata={
            "sender_username": _user["username"],
            "sender_id": _id,
            "receiver_username": user["username"],
            "receiver_id": user["_id"]
        },
        time=f"{today.day}/{today.month}/{today.year} {time.strftime('%H:%M:%S')}",
        status="sended",
        approved=False,
        ingoing=True
    ).dict()
    
    _request= _friend_request.copy()
    _request["ingoing"] = False

    #  user / _friend_request - user who we want add to friend
    # _user /        _request - we

    await insert_many("requests_db", [_request, _friend_request])
    
    return {"message": "ok."}


@social.get("/addfriend/{user_id}/accept")
async def accept_friendship_event(user_id, request: Request):
    # user_id = sender
    # _user _id = receiver, human who accept friend request
    auth_header = request.headers.get('Authorization')
    
    _id = (await FastJWT().decode(auth_header))["_id"]

    _user = await find_one("users_db", {"_id": _id})

    _key = "username"

    if await represents_int(user_id):
        user_id = int(user_id)
        _key = "_id"

    user = await find_one("users_db", {_key: user_id})

    if _user == user:
        return await self_error()

    if not user:
        return await user_does_not_exist_error()

    if not await find_one("requests_db", {
        "sender": user["_id"],
        "receiver": _id,
        "ingoing": False 
    }):
        return await request_not_found()
    
    if user["_id"] in _user["friends"]:
        return await already_friends_error()

    _user["friends"].append(user["_id"])
    user["friends"].append(_id)

    await delete_one("requests_db", {
        "sender": user["_id"],
        "receiver": _id,
        "ingoing": True
    })
    await delete_one("requests_db", {
        "sender": user["_id"],
        "receiver": _id,
        "ingoing": False 
    })

    await update_one("users_db", {"_id":_id}, _user)
    await update_one("users_db", {"_id": user["_id"]}, user)

    return {"message": "ok."}


@social.get("/feed")
async def generate_feed_event(request: Request):
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)