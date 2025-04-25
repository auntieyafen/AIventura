from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    google_maps_api_key: str
    serper_api_key: str
    serper_endpoint: str
    openweather_key: str
    openai_api_key: str
    openai_api_base: str

    class Config:
        env_file = ".env"

settings = Settings()
