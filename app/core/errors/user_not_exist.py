from fastapi import HTTPException

async def user_does_not_exist_error(message="Sorry, user does not exist."):
    raise HTTPException(status_code=404, detail=message)