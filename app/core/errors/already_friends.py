
from fastapi import HTTPException

async def already_friends_error(message="Sorry, you already friends."):
    raise HTTPException(status_code=400, detail=message)