"""
Weather Tools for IBM watsonx Orchestrate ADK
This tool provides weather information for cities.
"""
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from typing import Optional
import random

@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        Current weather information including temperature and conditions
    """
    # Mock weather data - in production, this would call a real weather API
    conditions = ["sunny", "partly cloudy", "cloudy", "rainy", "clear"]
    temperatures = list(range(60, 85))
    
    condition = random.choice(conditions)
    temp = random.choice(temperatures)
    
    return f"The weather in {city} is {condition} with a temperature of {temp}°F"

@tool
def get_forecast(city: str, days: int = 3) -> str:
    """
    Get weather forecast for a city.
    
    Args:
        city: The name of the city to get forecast for
        days: Number of days to forecast (default: 3)
        
    Returns:
        Weather forecast information
    """
    if days > 7:
        days = 7
    
    return f"Getting {days}-day weather forecast for {city}. In production, this would return detailed forecast data."
