from flask import request
from flask import redirect


class APIError(Exception):
    def __init__(self, code: int, message: str, logout_required: bool = False) -> None:
        super().__init__()
        self.code = code
        self.message = message
        self.logout_required = logout_required


def handle_api_error(error: APIError):
    return {
        "status": False,
        "message": error.message,
        "logout_required": error.logout_required
    }, error.code


def validation_error(error):
    del error
    return {
        "status": False,
        "message": "요청이 올바르지 않습니다.",
    }, 400


def not_found_error(error):
    return redirect(
        "/#" + request.path 
    )
