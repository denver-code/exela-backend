from app.core.internal.database import find

async def generate_id(db="users_db"):
    elements = await find(db, {})
    
    if not len(elements):
        return 1
    return elements[-1]["_id"] + 1