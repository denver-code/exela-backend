import re
from typing import Optional

from pydantic import (
    BaseModel
)


class GroupSchema(BaseModel):
    name: str
    alias: str
    tags: str
    description: str
