from typing import Optional

from pydantic import BaseModel


def timestamp(stamp):
    if stamp is None:
        return None

    return int(stamp.timestamp())


class TodoResponse(BaseModel):
    id: int
    checked: bool
    text: str
    created_at: int
    checked_at: Optional[int]
