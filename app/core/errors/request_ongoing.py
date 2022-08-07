from fastapi import HTTPException

async def request_ongoing(message="Sorry, request is ongoing, please wait for finish."):
    raise HTTPException(status_code=400, detail=message)