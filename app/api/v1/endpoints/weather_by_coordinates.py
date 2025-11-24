# app/api/v1/endpoints/weather_by_coordinates.py
from fastapi import APIRouter, Depends, HTTPException, Query
from httpx import HTTPStatusError
from app.core.config import Settings, get_settings
from app.services.weather_service import WeatherService
from app.models.weather import CurrentWeatherResponse

router = APIRouter()

@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(
    lat: float = Query(..., description="Latitude, e.g. 28.6139"),
    lon: float = Query(..., description="Longitude, e.g. 77.2090"),
    settings: Settings = Depends(get_settings),
):
    """
    Get current weather by coordinates.
    Example: /api/v1/weather/current?lat=28.6139&lon=77.2090
    """
    service = WeatherService(
        base_url=settings.WEATHER_API_BASE_URL,
        timeout=settings.WEATHER_API_TIMEOUT,
        api_key=settings.WEATHER_API_KEY
    )
    try:
        result = await service.get_current_weather(lat=lat, lon=lon)
    except RuntimeError as exc:
        # Missing API key or other runtime error
        raise HTTPException(status_code=500, detail=str(exc))
    except HTTPStatusError as exc:
        # Upstream returned non-2xx status
        raise HTTPException(status_code=502, detail=f"Upstream API error: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    # Build and return the Pydantic model
    return CurrentWeatherResponse.parse_obj({
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "temperature_c": result.get("temperature"),
        "windspeed": result.get("windspeed"),
        "raw": result.get("raw"),
    })
