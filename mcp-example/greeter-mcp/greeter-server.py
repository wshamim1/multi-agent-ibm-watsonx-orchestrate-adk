"""
MCP Greetings Server
A Model Context Protocol server that provides greeting and time-based functionality
"""
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from datetime import datetime
import pytz
import random

mcp = FastMCP("Greetings")

# List of greeting styles
GREETING_STYLES = {
    "formal": ["Good day", "Greetings", "Hello"],
    "casual": ["Hey", "Hi", "What's up", "Howdy"],
    "enthusiastic": ["Hey there!", "Hello!", "Hi there!", "Greetings!"],
    "professional": ["Good morning", "Good afternoon", "Good evening"]
}

@mcp.tool()
def greetme(name: str, style: str = "casual") -> str:
    """
    Greet a person by name with a specific style.
    
    Args:
        name: The name of the person to greet
        style: The greeting style (formal, casual, enthusiastic, professional)
    
    Returns:
        A personalized greeting message
    """
    print(f"Greeting {name} with {style} style")
    
    # Get greeting based on style
    greetings = GREETING_STYLES.get(style, GREETING_STYLES["casual"])
    greeting = random.choice(greetings)
    
    return f"{greeting} {name}! Welcome to the MCP Greetings System! 👋"

@mcp.tool()
def greet_with_time(name: str, timezone: str = "UTC") -> str:
    """
    Greet a person with the current time in their timezone.
    
    Args:
        name: The name of the person to greet
        timezone: The timezone (e.g., 'America/New_York', 'Europe/London', 'Asia/Tokyo')
    
    Returns:
        A greeting with current time information
    """
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        time_str = current_time.strftime("%I:%M %p")
        date_str = current_time.strftime("%B %d, %Y")
        
        # Determine time-based greeting
        hour = current_time.hour
        if 5 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        elif 17 <= hour < 21:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good night"
        
        return f"{time_greeting} {name}! 🌟 It's {time_str} on {date_str} in {timezone}."
    except Exception as e:
        return f"Hello {name}! (Note: Could not get time for timezone '{timezone}': {str(e)})"

@mcp.tool()
def greet_multiple(names: str, separator: str = ",") -> str:
    """
    Greet multiple people at once.
    
    Args:
        names: Comma-separated list of names (or use custom separator)
        separator: The separator used between names (default: comma)
    
    Returns:
        A greeting for all people
    """
    name_list = [name.strip() for name in names.split(separator) if name.strip()]
    
    if not name_list:
        return "Hello everyone! 👋"
    
    if len(name_list) == 1:
        return f"Hello {name_list[0]}! 👋"
    elif len(name_list) == 2:
        return f"Hello {name_list[0]} and {name_list[1]}! 👋"
    else:
        all_but_last = ", ".join(name_list[:-1])
        return f"Hello {all_but_last}, and {name_list[-1]}! 👋"

@mcp.tool()
def get_greeting_stats() -> str:
    """
    Get information about available greeting styles and timezones.
    
    Returns:
        Information about the greeting system capabilities
    """
    styles = ", ".join(GREETING_STYLES.keys())
    common_timezones = [
        "America/New_York", "America/Los_Angeles", "America/Chicago",
        "Europe/London", "Europe/Paris", "Asia/Tokyo", "Asia/Shanghai",
        "Australia/Sydney", "UTC"
    ]
    tz_list = ", ".join(common_timezones)
    
    return f"""
📊 MCP Greetings System Information:

Available Greeting Styles: {styles}

Common Timezones: {tz_list}

Tools Available:
- greetme: Basic greeting with style options
- greet_with_time: Time-aware greeting with timezone support
- greet_multiple: Greet multiple people at once
- get_greeting_stats: This information

Example Usage:
- greetme(name="John", style="formal")
- greet_with_time(name="Sarah", timezone="America/New_York")
- greet_multiple(names="Alice, Bob, Charlie")
"""

if __name__ == "__main__":
    print("=" * 60)
    print("MCP Greetings Server")
    print("=" * 60)
    print("Server is running using stdio transport...")
    print("Available tools: greetme, greet_with_time, greet_multiple, get_greeting_stats")
    print("=" * 60)
    mcp.run(transport="stdio")