class VerifyFail(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__()
        self.reason = reason


def handle_error_with_reason(error):
    return error.reason, 400
