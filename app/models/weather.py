# app/models/weather.py
from pydantic import BaseModel
from typing import Optional, Any

class CurrentWeatherResponse(BaseModel):
    """
    Response model for the endpoints. FastAPI will use this to:
      - validate returned data
      - generate API docs (Swagger)
    """
    latitude: Optional[float]
    longitude: Optional[float]
    temperature_c: Optional[float]
    windspeed: Optional[float]
    raw: Optional[Any]
