# import os
# import sys 
# from dotenv import load_dotenv


# load_dotenv()

# ALERT_WEBHOOK_URL = os.getenv("ALERT_WEBHOOK_URL")
# ALERT_THRESHOLD = int(os.getenv("ALERT_THRESHOLD", 3))
# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# if not ALERT_WEBHOOK_URL:
#     sys.exit("Error: ALERT_WEBHOOK_URL is required for sending alerts.")

from pathlib import Path
import sys
from pydantic import Field, HttpUrl, SecretStr, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).parent / ".env"

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH, 
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        )
    alert_webhook_url: HttpUrl 

    alert_threshold: int = Field(default=3, ge=1, le=100)

    log_level: str = Field(default="INFO")

try:
    config = Config() # type: ignore
except ValidationError as e:
    sys.exit(f"Configuration validation error: \n{e}")
   