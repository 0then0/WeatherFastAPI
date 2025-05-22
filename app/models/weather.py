from pydantic import BaseModel


class WeatherResponse(BaseModel):
    City: str
    Coordinates: str
    Current_apparent_temperature: str
    Current_temperature: str
    Current_weather_code: int
    Current_wind_speed: str
    Last_update: str
    Weather_description: str
