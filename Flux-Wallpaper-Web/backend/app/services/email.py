import httpx
from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.core.config import settings
from pathlib import Path

# Initialize SMTP configuration (Fallback)
use_ssl = settings.MAIL_PORT == 465
use_tls = settings.MAIL_PORT == 587

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM if settings.MAIL_FROM else settings.MAIL_USERNAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
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
        self.api_key = settings.EMAIL_API_KEY
        self.sender = {"name": settings.MAIL_FROM_NAME, "email": settings.MAIL_FROM}

    async def send_email(
        self,
        subject: str,
        recipients: List[EmailStr],
        body: str,
        subtype: MessageType = MessageType.html
    ):
        """
        Send an email asynchronously. Uses Brevo HTTP API if key is present, else SMTP.
        """
        # 1. Try Brevo HTTP API first (No blocked ports!)
        if self.api_key:
            return await self._send_brevo(subject, recipients, body)

        # 2. Fallback to SMTP
        return await self._send_smtp(subject, recipients, body, subtype)

    async def _send_brevo(self, subject: str, recipients: List[str], html_content: str):
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "api-key": self.api_key,
            "content-type": "application/json"
        }
        payload = {
            "sender": self.sender,
            "to": [{"email": email} for email in recipients],
            "subject": subject,
            "htmlContent": html_content
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=payload, timeout=10.0)
                response.raise_for_status()
                return True
            except Exception as e:
                print(f"Brevo API Error: {e}")
                return False

    async def _send_smtp(self, subject: str, recipients: List[str], body: str, subtype: MessageType):
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
            print(f"SMTP Error: {e}")
            return False

email_service = EmailService()
