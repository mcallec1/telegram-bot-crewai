from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests
import logging

logger = logging.getLogger(__name__)

class WeatherInput(BaseModel):
    """Input for weather tool."""
    location: str = Field(..., description="The location to get weather for")

class WeatherTool(BaseTool):
    name: str = "Current Weather"
    description: str = "Get current weather for a location"
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, location: str) -> str:
        logger.info(f"Fetching weather for location: {location}")
        try:
            api_key = os.getenv("OPENWEATHER_API_KEY")
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
            logger.debug(f"Weather API URL: {url}")
            
            response = requests.get(url)
            data = response.json()
            logger.debug(f"Weather API response: {data}")
            
            if response.status_code == 200:
                logger.info("Successfully retrieved weather data")
                return f"The current weather in {data['name']} is {data['main']['temp']}°C with {data['weather'][0]['description']}."
            
            logger.error(f"Weather API error: {data.get('message', 'Unknown error')}")
            return f"Could not fetch weather for '{location}'"
        except Exception as e:
            logger.error(f"Weather error: {e}", exc_info=True)
            return f"Weather error: {e}"

weather_tool = WeatherTool() 