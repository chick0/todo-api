from typing import Optional

from pydantic import BaseModel


class NoticeResponse(BaseModel):
    id: int
    title: str
    text: str
    created_at: int
    updated_at: Optional[int]
