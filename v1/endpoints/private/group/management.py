from fastapi import (
    APIRouter,
    Request
)
from app.core.errors.access_denied import access_denied
from app.core.errors.user_exist_error import user_exist_error
from app.core.errors.user_not_exist import user_does_not_exist_error
from app.core.internal.database import delete_one, find, find_one, update_one
from app.core.internal.fast_jwt import FastJWT
from app.core.models.group_model import Group
from app.core.schemas.group_schemas import GroupSchema


management = APIRouter()


@management.post("/")
async def create_group_group(_group: GroupSchema,request: Request):
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    _group = _group.dict()

    if await find_one("groups_db", {"name": _group["name"]}):
        return await user_exist_error("Sorry, group name already taken, try another.")

    _group["tags"] = list(map(lambda x: x.lower(), list(map(str.strip,  _group["tags"].split(",")))))
    _group["creator"] = int(_user["_id"])
    _group["participants"] = [int(_user["_id"])]
    _group["admins"] = [int(_user["_id"])]

    group = await Group().parse_obj(_group).create()

    return group


@management.delete("/{group_id}/")
async def delete_group_by_id(group_id: int, request: Request):
    group = await find_one("groups_db", {"_id": group_id})

    if not group:
        return await user_does_not_exist_error("Sorry, group does not exist.")

    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    if _user["_id"] != group["creator"]:
        return await access_denied()

    await delete_one("groups_db", {"_id": group_id})

    return {"message": "Success."}


@management.get("/")
async def get_groups_list():
    groups = await find("groups_db", {})

    return groups


@management.get("/{group_id}/")
async def get_event_by_id(group_id: int):
    group = await find_one("groups_db", {"_id": group_id})
    if group:
        return group
    return await user_does_not_exist_error("Sorry, group does not exist.")


@management.get("/{group_id}/join")
async def join_to_group(group_id: int, request: Request):
    group = await find_one("groups_db", {"_id": group_id})

    if not group:
        return await user_does_not_exist_error("Sorry, group does not exist.")

    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    if _user["_id"] in group["participants"]:
        return await user_exist_error("Sorry, user already in group.")
    
    group["participants"].append(_user["_id"])
    await update_one("groups_db", {"_id": group_id}, group)

    return {"message": "Success."}


@management.get("/{group_id}/leave")
async def leave_from_group(group_id: int, request: Request):
    group = await find_one("groups_db", {"_id": group_id})

    if not group:
        return await user_does_not_exist_error("Sorry, group does not exist.")

    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    if _user["_id"] == group["creator"]:
        return await access_denied("Sorry, but creator can't leave from group.")

    if _user["_id"] not in group["participants"]:
        return await user_exist_error("Sorry, user does not joined to group.")
    
    group["participants"].remove(_user["_id"])
    await update_one("groups_db", {"_id": group_id}, group)

    return {"message": "Success."}


@management.get("/my")
async def my_group_list(request: Request):
    auth_header = request.headers.get('Authorization')
    _user = await FastJWT().decode(auth_header)

    groups = await find("groups_db", {"participants": _user["_id"]})
    
    return groups
