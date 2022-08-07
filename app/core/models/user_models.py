from typing import  Optional
from pydantic import (
    BaseModel,
    Field
)

from app.core.internal.generate_id import generate_id
from app.core.internal.database import insert_one

class User(BaseModel):
    id: int = Field(None, alias='_id')
    
    username: Optional[str] = ""
    email: str
    password_hash: str

    first_name: Optional[str] = ""
    last_name: Optional[str] = "" 
    age: Optional[int] = 0
    biography: Optional[str] = ""
    sex: Optional[str] = "n" # m/f/n
    hobby: Optional[str] = ""
    tags: Optional[list] = []

    friends: Optional[list] = []
    # subscriptions: Optional[list] = []

    async def create(self):
        self.id = await generate_id()
        await insert_one("users_db", self.dict(by_alias=True))
        return self.dict(by_alias=True)