from fastapi import FastAPI,status,Depends
from fastapi.exceptions import HTTPException
from enum import Enum
from pydantic import BaseModel, Field
import requests

app = FastAPI()

class ProviderEnum(str, Enum):
    openweather = "openweather"
    openmeteo = "openmeteo"
    
class WeatherRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    provider: ProviderEnum    

# OpenWeather
def open_weather_provider(lat:float, lon:float):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": "3afdf767a1d084b9371ec344e8b50b6a"
    }
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenWeather unavailable"
        )

    return {
        "temp": float(data["main"]["temp"]) - 273.15,
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
    }

# OpenMeteo
def open_meteo_provider(lat:float, lon:float):
    
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenMeteo unavailable"
        )

    return {
        "temp": data["current"]["temperature_2m"],
        "humidity": data["current"]["relative_humidity_2m"],
        "wind_speed": data["current"]["wind_speed_10m"],
    }


@app.get("/weather")
async def get_weather(request: WeatherRequest= Depends()):
    if request.provider == ProviderEnum.openweather:
        return open_weather_provider(request.lat, request.lon)

    return open_meteo_provider(request.lat, request.lon)
