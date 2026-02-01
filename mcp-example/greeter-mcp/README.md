# MCP Greetings Server

A Model Context Protocol (MCP) server that provides intelligent greeting functionality with timezone awareness and multiple greeting styles.

## Features

✅ **Multiple Greeting Styles** - Formal, casual, enthusiastic, and professional
✅ **Timezone Support** - Time-aware greetings with timezone detection
✅ **Batch Greetings** - Greet multiple people at once
✅ **System Information** - Get details about available features
✅ **Easy Integration** - Works with IBM watsonx Orchestrate

## Tools Available

### 1. `greetme`
Basic greeting with customizable style.

**Parameters:**
- `name` (required): Person's name
- `style` (optional): Greeting style - `formal`, `casual`, `enthusiastic`, `professional`

**Example:**
```python
greetme(name="John", style="formal")
# Output: "Good day John! Welcome to the MCP Greetings System! 👋"
```

### 2. `greet_with_time`
Time-aware greeting with timezone support.

**Parameters:**
- `name` (required): Person's name
- `timezone` (optional): Timezone (default: UTC)

**Example:**
```python
greet_with_time(name="Sarah", timezone="America/New_York")
# Output: "Good morning Sarah! 🌟 It's 09:30 AM on January 29, 2026 in America/New_York."
```

### 3. `greet_multiple`
Greet multiple people at once.

**Parameters:**
- `names` (required): Comma-separated names
- `separator` (optional): Custom separator (default: comma)

**Example:**
```python
greet_multiple(names="Alice, Bob, Charlie")
# Output: "Hello Alice, Bob, and Charlie! 👋"
```

### 4. `get_greeting_stats`
Get information about the greeting system.

**Example:**
```python
get_greeting_stats()
# Returns system information and usage examples
```

## Installation

### 1. Install Dependencies

```bash
cd mcp
pip install -r requirements.txt
```

### 2. Test Locally

```bash
python3 GreetingsServer.py
```

## Deployment to IBM watsonx Orchestrate

### Quick Deploy

```bash
cd mcp
./manage_mcp_greeter.sh deploy
```

### Manual Steps

#### 1. Import Toolkit

```bash
orchestrate toolkits import \
    --kind mcp \
    --name greetme \
    --description "MCP toolkit that provides intelligent greeting functionality" \
    --package-root /path/to/mcp \
    --command "python3 GreetingsServer.py" \
    --app-id mcp_greeter_app
```

#### 2. Import Agent

```bash
orchestrate agents import -f greetermcp.yml
```

#### 3. Deploy Agent

```bash
orchestrate agents deploy --name greeterMCP
```

## Management Script

The `manage_mcp_greeter.sh` script provides easy management:

```bash
# Deploy everything
./manage_mcp_greeter.sh deploy

# Check status
./manage_mcp_greeter.sh status

# Test locally
./manage_mcp_greeter.sh test

# View help
./manage_mcp_greeter.sh help

# Remove everything
./manage_mcp_greeter.sh remove
```

## Common Timezones

- **US**: `America/New_York`, `America/Los_Angeles`, `America/Chicago`
- **Europe**: `Europe/London`, `Europe/Paris`, `Europe/Berlin`
- **Asia**: `Asia/Tokyo`, `Asia/Shanghai`, `Asia/Dubai`
- **Australia**: `Australia/Sydney`, `Australia/Melbourne`
- **UTC**: `UTC`

## Example Interactions

**Example 1: Basic Greeting**
```
User: Greet me, my name is John
Agent: Hey John! Welcome to the MCP Greetings System! 👋
```

**Example 2: Formal Greeting**
```
User: Give me a formal greeting for Sarah
Agent: Good day Sarah! Welcome to the MCP Greetings System! 👋
```

**Example 3: Time-based Greeting**
```
User: Greet Mike with the current time in New York
Agent: Good morning Mike! 🌟 It's 09:30 AM on January 29, 2026 in America/New_York.
```

**Example 4: Multiple People**
```
User: Greet Alice, Bob, and Charlie
Agent: Hello Alice, Bob, and Charlie! 👋
```

## Files

```
mcp/
├── GreetingsServer.py           # MCP server implementation
├── greetermcp.yml               # Agent configuration
├── requirements.txt             # Python dependencies
├── manage_mcp_greeter.sh       # Management script
└── README.md                    # This file
```

## Troubleshooting

### Import Errors

```bash
pip install --upgrade fastmcp pytz
```

### Server Not Starting

Check that all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Tool Not Found

Ensure the toolkit is imported before deploying the agent:
```bash
./manage_mcp_greeter.sh import-toolkit
./manage_mcp_greeter.sh import-agent
./manage_mcp_greeter.sh deploy-agent
```

## Development

### Add New Tools

Edit `GreetingsServer.py` and add new functions with the `@mcp.tool()` decorator:

```python
@mcp.tool()
def my_new_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"
```

### Update Agent Configuration

Edit `greetermcp.yml` to add new tools:

```yaml
tools:
- greetme:greetme
- greetme:my_new_tool
```

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [IBM watsonx Orchestrate](https://www.ibm.com/docs/en/watsonx/watson-orchestrate)

