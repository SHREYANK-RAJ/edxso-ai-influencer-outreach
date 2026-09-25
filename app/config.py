from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    youtube_api_key: str | None = None
    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"
    gmail_credentials_file: str = "credentials.json"
    gmail_token_file: str = "token.json"
    database_url: str = "sqlite:///./data/outreach.db"
    target_niche: str = "technology"
    min_followers: int = 5000
    max_followers: int = 100000
    min_engagement_rate: float = 1.0
    model_config = SettingsConfigDict(env_file=ROOT_DIR / ".env", extra="ignore")

settings = Settings()
