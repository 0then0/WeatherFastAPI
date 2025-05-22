from fastapi import APIRouter, HTTPException, Query

from app.models.weather import WeatherResponse
from app.services.weather_service import fetch_current_weather

router = APIRouter()


@router.get("/", response_model=WeatherResponse)
async def get_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    try:
        return await fetch_current_weather(lat, lon)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
