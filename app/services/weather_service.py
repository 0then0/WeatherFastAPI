from datetime import datetime

import httpx

from app.config import settings
from app.exceptions import WeatherAPIException
from app.models.weather import WeatherResponse
from app.services.geocoding_service import get_city_name

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Drizzle: Light",
    53: "Drizzle: Moderate",
    55: "Drizzle: Dense intensity",
    61: "Rain: Slight",
    63: "Rain: Moderate",
    65: "Rain: Heavy",
    66: "Freezing Rain: Light",
    67: "Freezing Rain: Heavy",
    71: "Snow fall: Slight",
    73: "Snow fall: Moderate",
    75: "Snow fall: Heavy",
    77: "Snow grains",
    80: "Rain showers: Slight",
    81: "Rain showers: Moderate",
    82: "Rain showers: Violent",
    85: "Snow showers: Slight",
    86: "Snow showers: Heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with hail: Slight",
    99: "Thunderstorm with hail: Heavy",
}


def format_coordinates(lat: float, lon: float) -> str:
    lat_str = f"{abs(lat):.4f}\u00b0{'N' if lat >= 0 else 'S'}"
    lon_str = f"{abs(lon):.4f}\u00b0{'E' if lon >= 0 else 'W'}"
    return f"Lat: {lat_str} Lon: {lon_str}"


async def fetch_current_weather(lat: float, lon: float) -> WeatherResponse:
    """
    Fetches current weather data and performs reverse-geocoding to determine city name.

    :param lat: Latitude for weather query
    :param lon: Longitude for weather query
    :return: WeatherResponse Pydantic model with formatted data
    :raises WeatherAPIException: On HTTP or data parsing errors from the weather API
    """
    city = await get_city_name(lat, lon)

    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "timezone": "auto",
    }

    try:
        async with httpx.AsyncClient(timeout=settings.TIMEOUT_SECONDS) as client:
            resp = await client.get(str(settings.OPEN_METEO_BASE_URL), params=params)
            resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise WeatherAPIException(
            f"Weather API error: {exc.response.status_code} {exc.response.reason_phrase}"
        )
    except httpx.RequestError as exc:
        raise WeatherAPIException(f"Weather API request failed: {exc}")

    data = resp.json()
    try:
        cw = data["current_weather"]
        temp = cw["temperature"]
        app_temp = cw.get("apparent_temperature", temp)
        wind = cw["windspeed"]
        code = cw["weathercode"]
        time = cw["time"]
    except KeyError:
        raise WeatherAPIException("Unexpected response format from weather service.")

    return WeatherResponse(
        City=city,
        Coordinates=format_coordinates(lat, lon),
        Current_apparent_temperature=f"{app_temp}\u00b0C",
        Current_temperature=f"{temp}\u00b0C",
        Current_weather_code=code,
        Current_wind_speed=f"{wind} km/h",
        Last_update=time,
        Weather_description=WEATHER_CODES.get(code, "Unknown"),
    )
