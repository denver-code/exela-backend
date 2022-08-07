from typing import  Optional
from pydantic import (
    BaseModel,
    Field
)


class FriendRequest(BaseModel):
    request_type: str = "friendship"

    sender: int
    receiver: int

    metadata: dict = {}

    time: str
    status: str
    approved: bool = False

    # meaning sended from youself. Made for finding diference between sended and recived requests.
    # True - if you recive this request
    ingoing: bool = True