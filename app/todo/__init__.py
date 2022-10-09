from typing import Optional

from pydantic import BaseModel

# todo const
MAX_TODO = 100


class TodoResponse(BaseModel):
    id: int
    checked: bool
    text: str
    created_at: int
    checked_at: Optional[int]
