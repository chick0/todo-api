from flask import request


class APIError(Exception):
    def __init__(self, code: int, message: str) -> None:
        super().__init__()
        self.code = code
        self.message = message


def handle_api_error(error):
    if request.path.startswith("/api/verify"):
        return error.message, error.code

    return {
        "status": False,
        "message": error.message
    }, error.code
