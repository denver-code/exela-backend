
from fastapi import HTTPException

async def access_denied(message="Sorry, access denied."):
    raise HTTPException(status_code=403, detail=message)