from fastapi import (
    APIRouter
)
from app.core.errors.invalid_credits import invalid_credits
from app.core.errors.user_not_exist import user_does_not_exist_error
from app.core.internal.fast_jwt import FastJWT

from app.core.schemas.user_schemas import AuthUserModel
from app.core.internal.database import find_one


signin = APIRouter(prefix="/signin")


@signin.post("/")
async def signin_event(user: AuthUserModel):
    user = user.dict()

    if not await find_one("users_db", {"email": user["email"]}):
        return await user_does_not_exist_error()

    _user = await find_one("users_db", {"email": user["email"]})

    if user["password_hash"] != _user["password_hash"]:
        return await invalid_credits()

    delete_objects = [
        "password_hash",
        "friends",
    ]

    for object in delete_objects:
        del _user[object]

    _jwt = await FastJWT().encode(_user)
    return {"auth_token": _jwt}