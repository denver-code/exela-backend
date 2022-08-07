from fastapi import HTTPException

async def invalid_credits(message="Sorry, email or password not correct."):
    raise HTTPException(status_code=400, detail=message)