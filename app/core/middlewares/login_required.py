import datetime

from fastapi import HTTPException, Header
from app.core.errors.unauthorized import need_authorization

from app.core.internal.fast_jwt import FastJWT


async def login_required(Authorization=Header("Authorization")):
        try:       
            jwt_token = await FastJWT().decode(Authorization)

            if jwt_token["expire"] < int(datetime.datetime.now().timestamp()):
                raise await need_authorization()

        except:
            raise await need_authorization()