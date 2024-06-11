from pathlib import Path
from os import environ
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from My_project.services.auth import create_email_token


conf = ConnectionConfig(
    MAIL_USERNAME= environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD= environ.get("MAIL_PASSWORD"),
    MAIL_FROM= environ.get("MAIL_FROM"),
    MAIL_PORT= environ.get("MAIL_PORT"),
    MAIL_SERVER= environ.get("MAIL_SERVER"),
    MAIL_FROM_NAME= environ.get("MAIL_FROM_NAME"),
    MAIL_STARTTLS= environ.get("MAIL_STARTTLS"),
    MAIL_SSL_TLS= environ.get("MAIL_SSL_TLS"),
    USE_CREDENTIALS= environ.get("USE_CREDENTIALS"),
    VALIDATE_CERTS= environ.get("VALIDATE_CERTS"),
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

async def send_email(email: EmailStr, username: str, host: str):
    """function send email"""
    try:
        token_verification = await create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message,template_name="email_template.html")
    except ConnectionErrors as e:
        print(f" Send_email ---- {e}")