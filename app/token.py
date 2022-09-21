from jwt import encode
from jwt import decode
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import DecodeError
from flask import current_app as app

from app.secret import get_secret
from app.error import APIError


def create_token(payload: dict, name: str) -> str:
    return encode(
        payload=payload,
        key=get_secret(name=name),
        algorithm=app.config.algorithms[0]
    )

def parse_token(token: str, name: str) -> dict:
    try:
        return decode(
            jwt=token,
            key=get_secret(name=name),
            algorithms=app.config.algorithms
        )
    except ExpiredSignatureError as e:
        raise APIError(
            code=401,
            message="만료된 토큰입니다.",
            logout_required=True
        ) from e
    except DecodeError as e:
        raise APIError(
            code=401,
            message="인증 토큰 검증 실패",
            logout_required=True
        ) from e
