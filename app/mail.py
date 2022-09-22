from os import environ
from smtplib import SMTP
from email.mime.text import MIMEText
from re import compile

from app.error import APIError

re = compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

SMTP_HOST = environ['SMTP_HOST']
SMTP_PORT = int(environ['SMTP_PORT'])
SMTP_USER = environ['SMTP_USER']
SMTP_PASSWORD = environ['SMTP_PASSWORD']


def test_email(email: str):
    if re.match(email) is None:
        raise APIError(
            code=400,
            message="해당 이메일 주소는 사용 할 수 없습니다."
        )


def send_mail(email: str, title: str, html: str):
    test_email(email=email)
    payload = MIMEText(html, "html", "utf-8")
    payload['From'] = SMTP_USER
    payload['Subject'] = title

    with SMTP(SMTP_HOST, SMTP_PORT) as client:
        client.starttls()
        client.login(
            user=SMTP_USER,
            password=SMTP_PASSWORD
        )

        client.sendmail(
            from_addr=SMTP_USER,
            to_addrs=[email],
            msg=payload.as_string()
        )
