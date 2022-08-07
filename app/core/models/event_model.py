import time
from datetime import datetime
from typing import  Optional
from pydantic import (
    BaseModel,
    Field
)

from app.core.internal.generate_id import generate_id
from app.core.internal.database import insert_one

class EventModel(BaseModel):
    id: int = Field(None, alias='_id')
    
    name: Optional[str] = ""
    alias: Optional[str] = "other"

    description: Optional[str] = ""
    status: Optional[str] = "active"
    organisator: Optional[str] = ""
    creator: Optional[int] = 0

    date: Optional[str] = f"{datetime.now().day}/{datetime.now().month}/{datetime.now().year} {time.strftime('%H:%M:%S')}"
    
    participants : Optional[list] = []

    async def create(self):
        self.id = await generate_id("events_db")
        await insert_one("events_db", self.dict(by_alias=True))
        return self.dict(by_alias=True)
        