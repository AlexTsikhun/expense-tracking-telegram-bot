from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str | None = None
    TELEGRAM_BOT_TOKEN: str
    API_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
