# FastAPI + Pydantic Mini Project

Two weather endpoints (OpenWeatherMap):

- GET `/api/v1/weather/current?lat=<>&lon=<>` — current weather by coordinates
- GET `/api/v1/weather/by_city?city=<>&country=<>` — current weather by city (optional country)

Setup so that I remeber :
1 `python -m venv .venv`
2. `pip install -r requirements.txt`
3. cpoy `.env.example` to `.env` and add your OpenWeatherMap API key
4.  `uvicorn app.main:app --reload --port 8000`
5. `http://127.0.0.1:8000/docs`



1) git init
2) git remote add origin https://github.com/sarangiswadha/fastapi-pydantic-mini.git'
3) git push -u origin main
