import re
from typing import Optional

from pydantic import (
    BaseModel,
    validator
)


class AuthUserModel(BaseModel):
    email: str
    password_hash: str


    @validator("email")
    def check_email_event(cls, v):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if not re.fullmatch(regex, v):
            raise ValueError("Invalid email")
        return v
    

    @validator("password_hash")
    def check_password_hash_event(cls, v):
        regex = r"^[a-fA-F0-9]{64}$"
        if not re.fullmatch(regex, v):
            raise ValueError("Invaid password hash")
        return v


class UserProfile(BaseModel):
    username: Optional[str] = ""

    first_name: Optional[str] = ""
    last_name: Optional[str] = "" 
    age: Optional[int] = 0
    biography: Optional[str] = ""
    hobby: Optional[str] = ""
    tags: Optional[str] = ""
    sex: Optional[str] = "n" # m/f/n


    @validator('username')
    def check_username_event(cls, v):
        regex = r"^.*[a-zA-Z]+.*$"
        if not re.fullmatch(regex, v):
            raise ValueError("Invaid username. Username must contain more than 1 letter.")
        return v