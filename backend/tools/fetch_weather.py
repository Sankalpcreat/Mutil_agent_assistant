from langchain.tools import BaseTool
import requests
import os
from dotenv import load_dotenv

class FetchWeatherTool(BaseTool):
    name: str = "fetch_weather"
    description: str = "Fetch weather information for a given location."

    def __init__(self):
        super().__init__()
        load_dotenv()  

    def _run(self, location: str)->str:
        api_key = os.getenv("WEATHERSTACK_API_KEY")
        if not api_key:
            return "Weatherstack API key not found. Please set the WEATHERSTACK_API_KEY environment variable."

        url = f"http://api.weatherstack.com/current"
        params = {
            'access_key': api_key,
            'query': location,
            'units': 'm' 
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  
            data = response.json()
            if 'error' in data:
                return f"Error fetching weather data: {data['error']['info']}"
            weather_desc = data["current"]["weather_descriptions"][0]
            temp = data["current"]["temperature"]
            return f"The current weather in {location} is {weather_desc} with a temperature of {temp}°C."
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"

    async def _arun(self, location: str)->str:
        raise NotImplementedError("Async not implemented for FetchWeatherTool.")
