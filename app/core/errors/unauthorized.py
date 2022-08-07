from fastapi import HTTPException

async def need_authorization(message="Unauthorized. Please add Authorization token to Headers."):
    raise HTTPException(status_code=401, detail=message)