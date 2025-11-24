# FastAPI + Pydantic Mini Project

Two weather endpoints (OpenWeatherMap):

- GET `/api/v1/weather/current?lat=<>&lon=<>` — current weather by coordinates
- GET `/api/v1/weather/by_city?city=<>&country=<>` — current weather by city (optional country)

Setup:
1. Create a virtual env: `python -m venv .venv`
2. Activate it and install deps: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your OpenWeatherMap API key
4. Run: `uvicorn app.main:app --reload --port 8000`
5. Open docs: `http://127.0.0.1:8000/docs`
