from fastapi import HTTPException

async def request_not_found(message="Sorry, request not found."):
    raise HTTPException(status_code=404, detail=message)