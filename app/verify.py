from datetime import datetime
from datetime import timedelta

from jwt import encode

from app.secret import get_secret

algorithms = ["HS256"]


def create_token(email: str) -> str:
    return encode(
        payload={
            "email": email,
            "exp": int((datetime.now() + timedelta(days=1)).timestamp())
        },
        key=get_secret("email_verify"),
        algorithm=algorithms[0]
    )


def send_verify_request(email: str) -> bool:
    token = create_token(email=email)

    # TODO: Sendmail

    return False
