## Simple Weather API

This is a simple FastAPI-based backend service that fetches current weather data and reverse-geocodes city names using the Open-Meteo and OpenStreetMap Nominatim APIs. It exposes a single API endpoint to retrieve user-friendly weather information for any given latitude and longitude.

---

### Prerequisites

- Python 3.10+
- Internet access to call external APIs

---

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/0then0/WeatherFastAPI
   cd WeatherFastAPI
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .\.venv\Scripts\activate # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

### Configuration

Create a `.env` file at the project root with the following variables:

```dotenv
# Open-Meteo API endpoint
OPEN_METEO_BASE_URL=https://api.open-meteo.com/v1/forecast

# Nominatim reverse-geocoding endpoint
GEOCODING_BASE_URL=https://nominatim.openstreetmap.org/reverse

# HTTP client timeout in seconds
TIMEOUT_SECONDS=10

# User-Agent header for Nominatim
USER_AGENT=WeatherFastAPI
```

These values are loaded and validated by `app/config.py` using `pydantic-settings`.

---

### Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

By default, the server runs at `http://localhost:8000`.

---

### API Endpoint

#### Get Current Weather

```
GET /weather?lat=<latitude>&lon=<longitude>
```

**Query Parameters**

| Parameter | Type  | Required | Description               |
| --------- | ----- | -------- | ------------------------- |
| `lat`     | float | Yes      | Latitude of the location  |
| `lon`     | float | Yes      | Longitude of the location |

**Response JSON**

```json
{
	"City": "San Francisco",
	"Coordinates": "Lat: 37.7749°N Lon: -122.4194°E",
	"Current_apparent_temperature": "7.1°C",
	"Current_temperature": "9.3°C",
	"Current_weather_code": 3,
	"Current_wind_speed": "10.8 km/h",
	"Last_update": "2025-03-22T14:45:00",
	"Weather_description": "Overcast"
}
```

- **`City`**: Human-readable city name via reverse geocoding.
- **`Coordinates`**: Echoed location with degree symbols.
- **`Current_*`**: Weather metrics (temperature, wind speed, code).
- **`Last_update`**: Timestamp of the weather data.
- **`Weather_description`**: Mapped from the weather code.
