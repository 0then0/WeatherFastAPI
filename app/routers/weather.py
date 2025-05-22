from fastapi import APIRouter, HTTPException, Query

from app.exceptions import GeocodingException, WeatherAPIException
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
    except GeocodingException as ge:
        # Upstream service failed: client error 424
        raise HTTPException(status_code=424, detail=str(ge))
    except WeatherAPIException as we:
        # Upstream service failed: bad gateway
        raise HTTPException(status_code=502, detail=str(we))
    except Exception as e:
        # Catch-all for anything unexpected
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
