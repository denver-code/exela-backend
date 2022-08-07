from fastapi import (
    APIRouter
)
from v1.endpoints.public.authorization.signin import signin
from v1.endpoints.public.authorization.signup import signup


authorization = APIRouter(prefix="/authorization")


authorization.include_router(signin)
authorization.include_router(signup)
