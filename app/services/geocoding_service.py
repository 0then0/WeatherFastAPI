import httpx

from app.config import settings


async def get_city_name(lat: float, lon: float) -> str:
    """
    Calls Nominatim reverse-geocoding to turn coordinates into a city/locality name.
    Returns the 'city' or falls back to 'town' or 'village' or 'county'.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "zoom": 10,  # city-level
        "addressdetails": 1,  # include detailed fields
    }
    headers = {"User-Agent": settings.USER_AGENT}

    async with httpx.AsyncClient(timeout=settings.TIMEOUT_SECONDS) as client:
        resp = await client.get(
            str(settings.GEOCODING_BASE_URL),
            params=params,
            headers=headers,
        )
        resp.raise_for_status()
        data = resp.json()

    addr = data.get("address", {})
    # Prefer city > town > village > county
    return (
        addr.get("city")
        or addr.get("town")
        or addr.get("village")
        or addr.get("county")
        or "Unknown location"
    )
