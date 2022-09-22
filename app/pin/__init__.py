from secrets import token_bytes

from pydantic import BaseModel

from app.token import create_token as ct
from app.token import parse_token as pt

name = "auth:pin"


class PinToken(BaseModel):
    pid: int
    uid: int
    randstring: str


def create_token(pid: int, uid: int) -> str:
    return ct(
        payload=PinToken(
            pid=pid,
            uid=uid,
            randstring=token_bytes(8).hex()
        ).dict(),
        name=name
    )


def parse_token(token: str) -> PinToken:
    return PinToken(**pt(token, name))
