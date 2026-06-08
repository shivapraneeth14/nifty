from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    supabase_url: str = ""
    supabase_service_key: str = ""
    supabase_anon_key: str = ""
    hf_api_token: str = ""
    hf_model_url: str = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    app_env: str = "development"
    debug: bool = True

    class Config:
        env_file = Path(__file__).parent.parent.parent / ".env"
        extra = "ignore"


settings = Settings()
