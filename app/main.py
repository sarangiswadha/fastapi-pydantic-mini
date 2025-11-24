# app/main.py
from fastapi import FastAPI
from app.core.logging_config import configure_logging
from app.api.v1.endpoints import weather_by_coordinates, weather_by_city

# Configure logging early
configure_logging()

app = FastAPI(title="FastAPI + Pydantic Mini Project", version="0.1.0")

# Include routers for each endpoint file. Both are mounted under the same prefix
# so their paths become:
#  - /api/v1/weather/current
#  - /api/v1/weather/by_city
app.include_router(
    weather_by_coordinates.router,
    prefix="/api/v1/weather",
    tags=["weather-coordinates"]
)
app.include_router(
    weather_by_city.router,
    prefix="/api/v1/weather",
    tags=["weather-city"]
)


@app.get("/")
async def root():
    """Simple root endpoint to check if the app is running."""
    return {"message": "FastAPI + Pydantic Mini Project. See /docs for API docs."}
