class APIError(Exception):
    def __init__(self, code: int, message: str, logout_required: bool = False, **kwargs) -> None:
        super().__init__()
        self.code = code
        self.message = message
        self.logout_required = logout_required
        self.kwargs = kwargs


def handle_api_error(error: APIError):
    return {
        "status": False,
        "message": error.message,
        "logout_required": error.logout_required
    }, error.code


def validation_error(error):
    del error
    return handle_api_error(
        APIError(
            code=400,
            message="요청이 올바르지 않습니다."
        )
    )


def not_found_error(error):
    del error
    return handle_api_error(
        APIError(
            code=404,
            message="올바른 경로가 아닙니다."
        )
    )
