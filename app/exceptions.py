class WeatherAPIException(Exception):
    """Raised when fetching weather data fails."""

    pass


class GeocodingException(Exception):
    """Raised when reverse-geocoding fails."""

    pass
