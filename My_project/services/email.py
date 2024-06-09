from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from My_project.services.auth import create_email_token


conf = ConnectionConfig(
    MAIL_USERNAME="veslo7601@meta.ua",
    MAIL_PASSWORD="Q12345Rr",
    MAIL_FROM="veslo7601@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Example email",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

async def send_email(email: EmailStr, username: str, host: str):
    """function send email"""
    try:
        token_verification = await create_email_token({"sub": email})
        print(f"Токен стоврений ----- {token_verification}")
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message,template_name="email_template.html")
        print(f"Токен переданий ----- {token_verification}")
    except ConnectionErrors as e:
        print(f" Send_email ---- {e}")