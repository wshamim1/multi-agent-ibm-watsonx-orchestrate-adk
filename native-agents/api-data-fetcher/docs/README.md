# API Data Fetcher Agent with Basic Connections

This example demonstrates how to create IBM Watsonx agents that utilize **basic authentication connections** to fetch and process data from external APIs.

## Overview

This example includes:
- **FastAPI Backend Server** - Real API with basic authentication ([see FASTAPI_README.md](FASTAPI_README.md))
- **Data Fetcher Agent** ([`agents/data_fetcher_agent.yaml`](../agents/data_fetcher_agent.yaml)) - Fetches data from external APIs using basic authentication
- **Data Processor Agent** ([`agents/data_processor_agent.yaml`](../agents/data_processor_agent.yaml)) - Processes and analyzes the fetched data
- **Supervisor Agent** ([`agents/supervisor_agent.yaml`](../agents/supervisor_agent.yaml)) - Coordinates between the two agents

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  User Request                        │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│           Supervisor Agent (Orchestrator)            │
└────────────┬───────────────────────┬─────────────────┘
             │                       │
             ▼                       ▼
┌────────────────────────┐  ┌──────────────────────┐
│  Data Fetcher Agent    │  │ Data Processor Agent │
│  (uses basic auth)     │  │ (processes results)  │
└───────────┬────────────┘  └──────────┬───────────┘
            │                          │
            ▼                          │
┌────────────────────────┐            │
│   FastAPI Backend      │            │
│   - Basic Auth         │            │
│   - Mock Data          │            │
│   - REST Endpoints     │            │
└───────────┬────────────┘            │
            │                         │
            └─────────────────────────┘
                      │
                      ▼
              User gets results
```

## Components

## Components

### Tools ([`tools/data_fetcher_tools.py`](../tools/data_fetcher_tools.py))

All tools use the `expected_credentials` decorator parameter to declare their connection requirements:

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections

MY_APP_ID = 'basic-connection-app'

@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def my_tool():
    # Fetch credentials at runtime
    creds = connections.basic_auth(MY_APP_ID)
    # Use creds.url, creds.username, creds.password
    ...
```

**Tools included:**
- `fetch_api_data`: Fetches data from API endpoints using basic authentication
- `fetch_user_info`: Retrieves user information from an API with authentication
- `search_api_data`: Searches data using query parameters with authentication

### Processing Tools (no authentication required)
- `process_api_response`: Processes and analyzes API response data
- `format_data_report`: Formats data into human-readable reports

### Agents
1. **data_fetcher_agent.yaml**: Handles API data retrieval with authentication
2. **data_processor_agent.yaml**: Processes and analyzes fetched data
3. **supervisor_agent.yaml**: Coordinates the overall workflow

## Prerequisites

1. **IBM Watsonx Orchestrate ADK** installed and configured
2. **Python 3.8+** with pip
3. **FastAPI Backend** (optional but recommended - see [FASTAPI_README.md](FASTAPI_README.md))
4. **Basic connection** set up in the connections folder
5. Valid credentials for the API you want to access

## Setup

### 1. Start the FastAPI Backend (Optional but Recommended)

For a complete working example, start the FastAPI backend server:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
./run_server.sh start-dev
# For local FastAPI server:
orchestrate connections set-credentials -a basic-connection-app \
  --env draft \
  -u demo \
  -p demo123

# For your own API:
orchestrate connections set-credentials -a basic-connection-app \
  --env draft \
  -u your_username \
  -p your_password
```

**Note**: If using the local FastAPI server, update the `server_url` in `basic-connections.yml` to `http://localhost:8000`

### 3FASTAPI_README.md](FASTAPI_README.md) for detailed server documentation.

### 2. Configure Basic Connection

First, set up the basic connection (if not already done):

```bash
# Navigate to the connections folder
cd ../../../connections

# Apply the basic connection configuration
orchestrate connections apply -f basic-connections.yml

# Set your API credentials
orchestrate connections set-credentials -a basic-connection-app \
  --env draft \
  -u your_username \
  -p your_password
```

### 2. Import and Deploy

Use the management script to import and deploy all components:

```bash
# Make the script executable
chmod +x scripts/manage_api_fetcher.sh

# Import all tools and agents
# Note: Tools will be automatically bound to basic-connection-app
./scripts/manage_api_fetcher.sh import-all

# Deploy all agents
./scripts/manage_api_fetcher.sh deploy-all

# Check status
./scripts/manage_api_fetcher.sh status
```

**Manual import (if needed):**

```bash
# Import tools with connection binding
orchestrate tools import -k python -f tools/data_fetcher_tools.py -a basic-connection-app

# Import agents
orchestrate agents import -f agents/data_fetcher_agent.yaml
orchestrate agents import -f agents/data_processor_agent.yaml
orchestrate agents import -f agents/supervisor_agent.yaml

# Deploy agents
orchestrate agents deploy -a data_fetcher_agent
orchestrate agents deploy -a data_processor_agent
orchestrate agents deploy -a api_data_supervisor_agent
```

## Usage

### Example Prompts

1. **Fetch user data**:
   ```
   Can you fetch user information for user ID 123?
   ```


4. **Dashboard metrics**:
   ```
   Get the dashboard metrics and show me a summary
   ```

See [Example_prompts.md](Example_prompts.md) for more examples.

### Testing with the FastAPI Backend

If you're running the local FastAPI server, you can test the integration:

1. **Start the FastAPI server**:
   ```bash
   cd backend
   ./run_server.sh start-background
   ```

2. **Verify the server is running**:
   ```bash
   ./run_server.sh status
   ./run_server.sh test-auth
   ```

### Testing with the FastAPI Backend

If you're running the local FastAPI server, you can test the integration:


**FastAPI Server Commands** (see [FASTAPI_README.md](FASTAPI_README.md)):

```bash
./run_server.sh start-dev       # Start with auto-reload
./run_server.sh start-background # Start in background
./run_server.sh status          # Check server status
./run_server.sh test-auth       # Test authentication
./run_server.sh stop            # Stop server
```
1. **Start the FastAPI server**:
   ```bash
   ./run_server.sh start-background
   ```

2. **Verify the server is running**:
   ```bash
   ./run_server.sh status
   ./run_server.sh test-auth
   ```

3. **Use the agents** to interact with the API:
   - The agents will automatically authenticate using the configured credentials
   - All requests will go to your local server
   - You can monitor requests in the server logs

4. **View server logs**:
   ```bash
   ./run_server.sh logs
   ```
2. **Search API data**:
   ```
   Search for all products with status "active"
   ```

3. **Complex workflow**:
   ```
   Fetch the data for user 456 and analyze their activity patterns
   ```

## Management Commands

The `manage_api_fetcher.sh` script provides several commands:

- `import-all`: Import all tools and agents
- `import-tools`: Import only the tools
- `import-agents`: Import only the agents
- `deploy-all`: Deploy all agents
- `undeploy-all`: Undeploy all agents
- `remove-all`: Remove all agents and tools
- `status`: Show current status

## Architecture

```
User Request
     ↓
Supervisor Agent
     ↓
     ├─→ Data Fetcher Agent (uses basic auth connection)
     │        ↓
     │   fetch_api_data / fetch_user_info / search_api_data
     │        ↓
     └─→ Data Processor Agent
              ↓
### How Connections Work in Tools

The tools use the official IBM Watsonx Orchestrate connection pattern:

1. **Declare expected credentials** in the `@tool` decorator:
   ```python
   @tool(
       expected_credentials=[
   **Update the connection configuration** in `../../connections/basic-connections.yml`:
   ```yaml
   server_url: https://your-api.example.com/
   ```

2. **Set your credentials**:
   ```bash
   orchestrate connections set-credentials -a basic-connection-app \
     --env draft \
     -u your_api_username \
     -p your_api_password
   ```

3. **Modify the tool functions** in [`tools/data_fetcher_tools.py`](../tools/data_fetcher_tools.py) to match your API endpoints

4. **Update the agent instructions** to reflect your use case

5. **Re-import the tools** with connection binding:
   ```bash
   orchestrate tools import -k python -f tools/data_fetcher_tools.py -a basic-connection-app
   ```

### Testing Locally

You can test your tools locally by setting environment variables:

```bash
# Set connection environment variables
export WXO_SECURITY_SCHEMA_basic_connection_app=basic_auth
export WXO_CONNECTION_basic_connection_app_url=https://your-api.example.com
export WXO_CONNECTION_basic_connection_app_username=your_username
export WXO_CONNECTION_basic_connection_app_password=your_password

# Run your Python script
python data_fetcher_tools.py
```

**Note:** The app_id must be sanitized by replacing non-alphanumeric characters with underscores in environment variable names.

2. **Fetch credentials at runtime** using the connections API:
   ```python
   from ibm_watsonx_orchestrate.run import connections
   
   creds = connections.basic_auth('basic-connection-app')
   url = creds.url
   username = creds.username
   password = creds.password
   ```

3. **Make authenticated requests** using the credentials:
   ```python
   from requests.auth import HTTPBasicAuth
   
   response = requests.get(
       url,
       auth=HTTPBasicAuth(creds.username, creds.password)
   )
   ```

4. **Bind connections during import** using the `-a` flag:
   ```bash
   orchestrate tools import -k python -f data_fetcher_tools.py -a basic-connection-app
   ```
```

## Connection Configuration

This example uses the `basic-connection-app` defined in `/connections/basic-connections.yml`:

```yaml
spec_version: v1
kind: connection
app_id: basic-connection-app
environments:
    draft:
        kind: basic
        type: team
        server_url: https://example.com/
```

The tools use this connection to authenticate API requests using username/password credentials.

## Customization

### Using with Your Own API

To adapt this example for your specific API:

1. Update the `server_url` in `basic-connections.yml` to point to your API
2. Modify the tool functions in `data_fetcher_tools.py` to match your API endpoints
3. Update the agent instructions to reflect your use case
4. Set your credentials using `orchestrate connections set-credentials`

### Adding New Tools

To add new tools:

1. Add new `@tool` decorated functions in `data_fetcher_tools.py`
2. Include the tool name in the appropriate agent YAML file
3. Re-import the tools and agents

## Troubleshooting

### Connection Issues

If you encounter authentication errors:

```bash
# Verify connection is applied
orchestrate connections list

# Re-set credentials
orchestrate connections set-credentials -a basic-connection-app \
  --env draft \
  -u your_username \
  -p your_password
```

### Agent Issues

```bash
# Check agent status
./manage_api_fetcher.sh status

# View agent logs
orchestrate agents logs data_fetcher_agent

# Re-deploy agents
./manage_api_fetcher.sh undeploy-all
./manage_api_fetcher.sh deploy-all
```

## Security Notes

- Never commit credentials to version control
- Use environment-specific credentials
- The basic connection credentials are stored securely by Orchestrate
- Consider using more secure authentication methods (OAuth, API keys) for production

## Next Steps

- Explore other connection types in the `/connections` folder
- Add error handling and retry logic to tools
- Implement data caching for frequently accessed endpoints
- Add validation for API responses

## References

- [IBM Watsonx Orchestrate Documentation](https://www.ibm.com/docs/en/watsonx/orchestrate)
- [ADK Connection Types](../../connections/README.md)
- [Agent Development Guide](../../README.md)
