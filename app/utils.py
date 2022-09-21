from flask import request


def get_ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr)


def timestamp(stamp) -> int or None:
    if stamp is None:
        return None

    return int(stamp.timestamp())
