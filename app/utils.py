from flask import request


def get_ip() -> str:
    return request.headers.get("X-Forwarded-For", request.remote_addr)
