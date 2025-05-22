from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPEN_METEO_BASE_URL: AnyUrl = Field(
        default="https://api.open-meteo.com/v1/forecast",
        description="Base URL for Open-Meteo API",
    )
    GEOCODING_BASE_URL: AnyUrl = Field(
        default="https://nominatim.openstreetmap.org/reverse",
        description="Base URL for reverse geocoding",
    )
    TIMEOUT_SECONDS: int = Field(default=10, gt=0)
    USER_AGENT: str = Field(
        default="WeatherFastAPI",
        description="User-Agent header for geocoding API",
    )

    class Config:
        env_file = ".env"


settings = Settings()
