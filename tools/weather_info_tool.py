import os
from typing import List

from dotenv import load_dotenv
from langchain.tools import tool

from exceptions.exceptionHandling import AppException
from utils.weather_info import WeatherForecastTool


class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY") or os.environ.get("OPENWEATHER_API_KEY")
        if self.api_key:
            os.environ.setdefault("OPENWEATHERMAP_API_KEY", self.api_key)
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""

        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a city"""
            if not self.api_key:
                return (
                    "Weather tool is not configured. Add `OPENWEATHERMAP_API_KEY` or "
                    "`OPENWEATHER_API_KEY`. Until then, tell the user you cannot provide live "
                    "weather and give only a clearly labeled general estimate if helpful."
                )

            try:
                weather_data = self.weather_service.get_current_weather(city)
                temp = weather_data.get("main", {}).get("temp", "N/A")
                desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
                return f"Current weather in {city}: {temp} deg C, {desc}"
            except AppException as exc:
                return exc.message

        @tool
        def get_weather_forecast(city: str) -> str:
            """Get weather forecast for a city"""
            if not self.api_key:
                return (
                    "Weather tool is not configured. Add `OPENWEATHERMAP_API_KEY` or "
                    "`OPENWEATHER_API_KEY`. Until then, tell the user you cannot provide a live "
                    "forecast and give only a clearly labeled general estimate if helpful."
                )

            try:
                forecast_data = self.weather_service.get_forecast_weather(city)
                if "list" in forecast_data:
                    forecast_summary = []
                    for item in forecast_data["list"]:
                        date = item["dt_txt"].split(" ")[0]
                        temp = item["main"]["temp"]
                        desc = item["weather"][0]["description"]
                        forecast_summary.append(f"{date}: {temp} degree celcius , {desc}")
                    return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
                return f"Could not fetch forecast for {city}"
            except AppException as exc:
                return exc.message

        return [get_current_weather, get_weather_forecast]
