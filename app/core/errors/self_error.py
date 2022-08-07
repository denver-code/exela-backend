from fastapi import HTTPException

async def self_error(message="You can't do it with youself."):
    raise HTTPException(status_code=400, detail=message)