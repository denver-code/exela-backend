import re
from typing import Optional

from pydantic import (
    BaseModel,
    validator
)


class EventSchema(BaseModel):
    name: str
    alias: str
    description: str
    organisator: str
    date: str
    