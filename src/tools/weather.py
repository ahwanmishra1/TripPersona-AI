import requests
from src.config.settings import settings


def get_weather(city: str) -> dict:
    if not settings.openweather_api_key:
        return {
            "status": "fallback",
            "summary": "Pleasant weather expected. Carry light cotton clothes and stay hydrated."
        }

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": settings.openweather_api_key,
            "units": "metric",
        }
        res = requests.get(url, params=params, timeout=8)
        res.raise_for_status()
        data = res.json()
        return {
            "status": "live",
            "summary": f"{data['weather'][0]['description']}, {data['main']['temp']}°C"
        }
    except Exception:
        return {
            "status": "fallback",
            "summary": "Weather unavailable right now. Plan for moderate daytime heat and light evening comfort."
        }