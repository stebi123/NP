from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

class Settings(BaseSettings):
    JWT_SECRET: str = Field(alias="JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    JWT_ALGORITHM: str
    
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_FOLDER: Path = BASE_DIR / "uploads" / "products"

    class Config:
        env_file = ".env"

settings = Settings()

# Create uploads directory if not exists
settings.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
