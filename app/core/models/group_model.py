from pydoc import describe
from typing import  Optional
from pydantic import (
    BaseModel,
    Field
)

from app.core.internal.generate_id import generate_id
from app.core.internal.database import insert_one

class Group(BaseModel):
    id: int = Field(None, alias='_id')
    
    name: Optional[str] = ""
    alias: Optional[str] = "other"
    tags: Optional[list] = []
    creator: Optional[int] = 1
    description: Optional[str] = ""
    participants: Optional[list] = []
    admins: Optional[list] = []

    async def create(self):
        self.id = await generate_id("groups_db")
        await insert_one("groups_db", self.dict(by_alias=True))
        return self.dict(by_alias=True)
        