from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    GOOGLE_MAPS_API_KEY: str
    SERPER_API_KEY: str
    SERPER_ENDPOINT: str
    OPENWEATHER_KEY: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str

    class Config:
        env_file = ".env"

settings = Settings()
