"""
Greeter Tools for IBM watsonx Orchestrate ADK
This tool provides greeting functionality.
"""
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def create_greeting(name: str) -> str:
    """
    Create a personalized greeting for a user.
    
    Args:
        name: The name of the person to greet
        
    Returns:
        A personalized greeting message
    """
    return f"Hey hi {name}, welcome to the Agent System!"

@tool
def format_greeting_with_weather(name: str, weather_info: str) -> str:
    """
    Format a complete greeting message with weather information.
    
    Args:
        name: The name of the person to greet
        weather_info: Weather information to include in the greeting
        
    Returns:
        A complete greeting message with weather
    """
    return f"Hey hi {name}, welcome to the Agent System! {weather_info}"

