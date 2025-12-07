from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.core.config import settings
from pathlib import Path

# Auto-detect SSL/TLS based on port
use_ssl = settings.MAIL_PORT == 465
use_tls = settings.MAIL_PORT == 587

# Initialize configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM if settings.MAIL_FROM else settings.MAIL_USERNAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER="smtp.googlemail.com", # Alternative hostname for better reliability
    MAIL_STARTTLS=use_tls,
    MAIL_SSL_TLS=use_ssl,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME or "Flux Depth Generator",
    TIMEOUT=60 
)

class EmailService:
    def __init__(self):
        self.fastmail = FastMail(conf)

    async def send_email(
        self,
        subject: str,
        recipients: List[EmailStr],
        body: str,
        subtype: MessageType = MessageType.html
    ):
        """
        Send an email asynchronously.
        """
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=subtype
        )
        
        try:
            await self.fastmail.send_message(message)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

email_service = EmailService()
