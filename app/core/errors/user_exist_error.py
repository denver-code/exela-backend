from fastapi import HTTPException

async def user_exist_error(message="Sorry, user already exist."):
    raise HTTPException(status_code=400, detail=message)