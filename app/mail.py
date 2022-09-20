from os import environ
from smtplib import SMTP
from email.mime.text import MIMEText

SMTP_HOST = environ['SMTP_HOST']
SMTP_PORT = int(environ['SMTP_PORT'])
SMTP_USER = environ['SMTP_USER']
SMTP_PASSWORD = environ['SMTP_PASSWORD']


def send_mail(email: str, title: str, html: str):
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
