import httpx

from app.config import settings
from app.exceptions import GeocodingException


async def get_city_name(lat: float, lon: float) -> str:
    params = {"lat": lat, "lon": lon, "format": "json", "zoom": 10, "addressdetails": 1}
    headers = {"User-Agent": settings.USER_AGENT}

    try:
        async with httpx.AsyncClient(timeout=settings.TIMEOUT_SECONDS) as client:
            resp = await client.get(
                str(settings.GEOCODING_BASE_URL), params=params, headers=headers
            )
            resp.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise GeocodingException(
            f"Geocoding API error: {exc.response.status_code} {exc.response.reason_phrase}"
        )
    except httpx.RequestError as exc:
        raise GeocodingException(f"Geocoding request failed: {exc}")

    data = resp.json()
    addr = data.get("address", {})
    if not addr:
        raise GeocodingException("No address details found in geocoding response.")

    return (
        addr.get("city")
        or addr.get("town")
        or addr.get("village")
        or addr.get("county")
        or "Unknown location"
    )
