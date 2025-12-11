# app/services/weather_service.py
import httpx
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Service that talks to OpenWeatherMap current weather endpoint.
    Provides:
      - get_current_weather(lat, lon)
      - get_current_by_city(city_name, country_code=None)
    """

    def __init__(self, base_url: str, timeout: int = 10, api_key: Optional[str] = None):
        """
        Initialize the service.

        Fix for AnyHttpUrl:
        If base_url comes from Pydantic AnyHttpUrl, convert to string
        before using string methods like rstrip().
        """
        self.base_url = str(base_url).rstrip("/")  # ✅ convert AnyHttpUrl to string
        self.timeout = timeout
        self.api_key = api_key

    async def _call_current_endpoint(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal helper to call the OpenWeatherMap 'weather' endpoint.
        Raises RuntimeError if API key is missing.
        """
        if not self.api_key:
            raise RuntimeError(
                "Missing WEATHER_API_KEY. Put your API key into the .env file or environment variables."
            )

        url = f"{self.base_url}/weather"
        params = params.copy()
        params["appid"] = self.api_key       # OpenWeatherMap API key
        params.setdefault("units", "metric") # Celsius temperature

        logger.debug("Calling OpenWeatherMap %s with %s", url, params)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()  # Raise exception if HTTP status is not 2xx
            return resp.json()

    async def get_current_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Get current weather by latitude & longitude.
        """
        data = await self._call_current_endpoint({"lat": lat, "lon": lon})
        coord = data.get("coord", {})
        main = data.get("main", {})
        wind = data.get("wind", {})
        return {
            "latitude": coord.get("lat"),
            "longitude": coord.get("lon"),
            "temperature": main.get("temp"),
            "windspeed": wind.get("speed"),
            "raw": data
        }

    async def get_current_by_city(self, city_name: str, country_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current weather by city name (optional country code).
        """
        q = city_name if not country_code else f"{city_name},{country_code}"
        data = await self._call_current_endpoint({"q": q})
        coord = data.get("coord", {})
        main = data.get("main", {})
        wind = data.get("wind", {})
        return {
            "latitude": coord.get("lat"),
            "longitude": coord.get("lon"),
            "temperature": main.get("temp"),
            "windspeed": wind.get("speed"),
            "raw": data
        }
