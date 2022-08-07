from fastapi import (
    APIRouter,
    Request
)
from app.core.errors.user_exist_error import user_exist_error

from app.core.errors.user_not_exist import user_does_not_exist_error
from app.core.internal.fast_jwt import FastJWT
from app.core.internal.database import find_one, update_one
from app.core.internal.represents_int import represents_int
from app.core.schemas.user_schemas import UserProfile


profile = APIRouter(prefix="/profile")


@profile.get("/me")
async def get_my_profile_event(request: Request):
    auth_header = request.headers.get('Authorization')
    
    _user = await FastJWT().decode(auth_header)

    user = await find_one("users_db", {"_id": _user["_id"]})
    del user["password_hash"]

    return {"result": user}


@profile.post("/me")
async def update_my_profile_event(user_profile: UserProfile, request: Request):
    auth_header = request.headers.get("Authorization")
    user_profile = user_profile.dict()
    
    if "username" in user_profile:
        if await find_one("users_db", {"username": user_profile["username"]}):
            return await user_exist_error("Sorry, username already taken, try another.")

    user_profile["tags"] = list(map(lambda x: x.lower(), list(map(str.strip,  user_profile["tags"].split(",")))))

    _user = await FastJWT().decode(auth_header)

    await update_one("users_db", {"_id":_user["_id"]}, user_profile)

    user = await find_one("users_db", {"_id": _user["_id"]})
    del user["password_hash"]

    return {"result": user}


@profile.get("/find/{user_id}")
async def find_user_event(user_id, request: Request):
    auth_header = request.headers.get('Authorization')

    delete_objects = [
        "password_hash",
    ]
    delete_objects_private = [
        "email",
        "first_name",
        "last_name",
        "age",
        "sex"
    ]
    count_replace_list = [
        "friends",
    ]

    _key = "username"

    if await represents_int(user_id):
        user_id = int(user_id)
        _key = "_id"

    _user = await find_one("users_db", {_key: user_id})

    if _user:

        _not_friends = True
        _id = (await FastJWT().decode(auth_header))["_id"]
        if _id in _user["friends"]:
            _not_friends = False 

        if _not_friends:
            for object in delete_objects_private:
                del _user[object]

        for object in delete_objects:
            del _user[object]
        
        for object in count_replace_list:
            _user[object] = len(_user[object])

        return {"result":_user}

    return await user_does_not_exist_error()
