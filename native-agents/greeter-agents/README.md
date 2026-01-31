# Greeter Agent System

A multi-agent system that creates personalized welcome messages with weather information.

## Overview

This system consists of three coordinated agents:

1. **Weather Agent** - Provides current weather information for cities
2. **Greeter Agent** - Creates personalized greeting messages
3. **Supervisor Agent** - Coordinates the weather and greeter agents to deliver complete welcome messages

## Architecture

```
User Input (Name + City)
         ↓
Greeter Supervisor Agent
         ↓
    ┌────┴────┐
    ↓         ↓
Weather    Greeter
Agent      Agent
    ↓         ↓
    └────┬────┘
         ↓
Complete Greeting Message
```

## Example Usage

**User Input:**
```
My name is John and I'm in New York
```

**System Output:**
```
Hey hi John, welcome to the Agent System! Today's weather in New York is sunny with a temperature of 72°F
```

## Components

### Weather Agent
- **Tools:** `get_weather`, `get_forecast`
- **Purpose:** Fetches current weather information for specified cities
- **File:** `weather_agent.yml`, `weather_tools.py`

### Greeter Agent
- **Tools:** `create_greeting`, `format_greeting_with_weather`
- **Purpose:** Creates personalized greeting messages
- **File:** `greeter_agent.yml`, `greeter_tools.py`

### Supervisor Agent
- **Collaborators:** `weather_agent`, `greeter_agent`
- **Purpose:** Coordinates both agents to create complete welcome messages
- **File:** `greeter_supervisor_agent.yml`

## Management Script

Use the `manage_greeter_system.sh` script to manage all components:

### Import Everything
```bash
./manage_greeter_system.sh import-all
```

### Deploy All Agents
```bash
./manage_greeter_system.sh deploy-all
```

### Check Status
```bash
./manage_greeter_system.sh status
```

### Remove Everything
```bash
./manage_greeter_system.sh remove-all
```

### Available Commands
- `import-all` - Import all tools and agents
- `import-tools` - Import only the tools
- `import-agents` - Import only the agents
- `deploy-all` - Deploy all agents
- `undeploy-all` - Undeploy all agents
- `remove-all` - Remove all agents and tools
- `remove-tools` - Remove all tools
- `remove-agents` - Remove all agents
- `status` - Show current status
- `help` - Display help message

## Workflow

1. **User provides name and city**
2. **Supervisor agent extracts information**
3. **Supervisor delegates to weather agent** to get weather for the city
4. **Weather agent returns weather information**
5. **Supervisor delegates to greeter agent** with name and weather info
6. **Greeter agent formats the complete message**
7. **Supervisor returns the final greeting to the user**

## Files

- `weather_agent.yml` - Weather agent configuration
- `weather_tools.py` - Weather tools implementation
- `greeter_agent.yml` - Greeter agent configuration
- `greeter_tools.py` - Greeter tools implementation
- `greeter_supervisor_agent.yml` - Supervisor agent configuration
- `manage_greeter_system.sh` - Management script
- `README.md` - This file

## Notes

- The weather data is currently mocked for demonstration purposes
- In production, the weather tools would integrate with a real weather API
- The supervisor agent coordinates the workflow automatically
- All agents use the watsonx LLM for natural language understanding
