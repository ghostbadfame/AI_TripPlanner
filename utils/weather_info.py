import requests

from exceptions.exceptionHandling import ExternalServiceError, ValidationError

class WeatherForecastTool:
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, place:str):
        """Get current weather of a place"""
        if not place or not place.strip():
            raise ValidationError("City name is required to fetch current weather.")

        if not self.api_key:
            raise ExternalServiceError("OpenWeather API key is not configured.")

        url = f"{self.base_url}/weather"
        params = {
            "q": place.strip(),
            "appid": self.api_key,
            "units": "metric",
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as exc:
            raise ExternalServiceError(
                "Weather service returned an error for the current weather request.",
                details={"city": place.strip(), "status_code": exc.response.status_code},
            ) from exc
        except requests.RequestException as exc:
            raise ExternalServiceError(
                "Unable to reach the weather service.",
                details={"city": place.strip()},
            ) from exc
    
    def get_forecast_weather(self, place:str):
        """Get weather forecast of a place"""
        if not place or not place.strip():
            raise ValidationError("City name is required to fetch weather forecast.")

        if not self.api_key:
            raise ExternalServiceError("OpenWeather API key is not configured.")

        url = f"{self.base_url}/forecast"
        params = {
            "q": place.strip(),
            "appid": self.api_key,
            "cnt": 10,
            "units": "metric",
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as exc:
            raise ExternalServiceError(
                "Weather service returned an error for the forecast request.",
                details={"city": place.strip(), "status_code": exc.response.status_code},
            ) from exc
        except requests.RequestException as exc:
            raise ExternalServiceError(
                "Unable to reach the weather service.",
                details={"city": place.strip()},
            ) from exc
