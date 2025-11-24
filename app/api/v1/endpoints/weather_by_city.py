# app/api/v1/endpoints/weather_by_city.py
from fastapi import APIRouter, Depends, HTTPException, Query
from httpx import HTTPStatusError
from typing import Optional
from app.core.config import Settings, get_settings
from app.services.weather_service import WeatherService
from app.models.weather import CurrentWeatherResponse

router = APIRouter()

@router.get("/by_city", response_model=CurrentWeatherResponse)
async def get_current_by_city(
    city: str = Query(..., description="City name, e.g. 'Delhi' or 'London'"),
    country: Optional[str] = Query(None, description="Optional 2-letter country code, e.g. 'IN', 'GB'"),
    settings: Settings = Depends(get_settings),
):
    """
    Get current weather by city name (optional country code).
    Example: /api/v1/weather/by_city?city=London&country=GB
    """
    service = WeatherService(
        base_url=settings.WEATHER_API_BASE_URL,
        timeout=settings.WEATHER_API_TIMEOUT,
        api_key=settings.WEATHER_API_KEY
    )
    try:
        result = await service.get_current_by_city(city_name=city, country_code=country)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream API error: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return CurrentWeatherResponse.parse_obj({
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "temperature_c": result.get("temperature"),
        "windspeed": result.get("windspeed"),
        "raw": result.get("raw"),
    })
