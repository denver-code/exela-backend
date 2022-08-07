from fastapi import (
    APIRouter
)
from app.core.errors.user_exist_error import user_exist_error
from app.core.internal.fast_jwt import FastJWT

from app.core.schemas.user_schemas import AuthUserModel
from app.core.models.user_models import User
from app.core.internal.database import find_one


signup = APIRouter(prefix="/signup")


@signup.post("/")
async def signup_event(user: AuthUserModel):
    user = user.dict()

    if await find_one("users_db", {"email": user["email"]}):
        return await user_exist_error("Sorry, email already taken, try another.")

    _user = User(
        email=user["email"],
        password_hash=user["password_hash"]
    )
    __user = await _user.create()

    delete_objects = [
        "password_hash",
        "friends",
    ]

    for object in delete_objects:
        del __user[object]

    _jwt = await FastJWT().encode(__user)
    return {"auth_token": _jwt}