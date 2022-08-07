from fastapi import(
    APIRouter
)

from v1.endpoints.private.user.profile import profile
from v1.endpoints.private.user.social import social 


user = APIRouter(prefix="/user")

user.include_router(profile)
user.include_router(social)