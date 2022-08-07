import time
from datetime import datetime
from typing import  Optional
from pydantic import (
    BaseModel,
    Field
)

from app.core.internal.generate_id import generate_id
from app.core.internal.database import insert_one

class MessageModel(BaseModel):
    id: int = Field(None, alias='_id')
    
    text: Optional[str] = ""
    alias: Optional[str] = "group"
    recipient: Optional[int] = 1
    sender: Optional[int] = 1
    metadata: Optional[dict] = {}

    date: Optional[str] = f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year} {time.strftime('%H:%M:%S')}"


    async def create(self, _db="groups_db"):
        self.id = await generate_id(_db)
        await insert_one(_db, self.dict(by_alias=True))
        return self.dict(by_alias=True)
        