import sys
import os
from pathlib import Path

# Add the project directory to sys.path
sys.path.append(str(Path(__file__).parent))

try:
    from app.core.config import settings
    # from app.core.mail import conf # This would fail without fastapi-mail installed
    print("Successfully imported settings.")
    print(f"MAIL_USERNAME: {settings.MAIL_USERNAME}")
    print(f"MAIL_SERVER: {settings.MAIL_SERVER}")
    print("Configuration loaded successfully (skipping fastapi-mail import check as it may not be installed).")
except Exception as e:
    print(f"Error loading configuration: {e}")
    sys.exit(1)
