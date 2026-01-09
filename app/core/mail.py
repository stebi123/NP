from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from app.core.config import settings
import asyncio

# SMTP configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)

# Low-level async email sender
async def _send_email(subject: str, recipients: list[EmailStr], body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)


# Public function used by auth router (SYNC SAFE)
def send_reset_email(email: str, token: str):
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    subject = "Reset your password"
    body = f"""
    <p>You requested a password reset.</p>
    <p>Click the link below to reset your password:</p>
    <p><a href="{reset_link}">Reset Password</a></p>
    <p>If you did not request this, you can safely ignore this email.</p>
    """

    try:
        # If FastAPI event loop is running
        loop = asyncio.get_running_loop()
        loop.create_task(
            _send_email(
                subject=subject,
                recipients=[email],
                body=body,
            )
        )
    except RuntimeError:
        # Fallback (should rarely happen, but safe)
        asyncio.run(
            _send_email(
                subject=subject,
                recipients=[email],
                body=body,
            )
        )
