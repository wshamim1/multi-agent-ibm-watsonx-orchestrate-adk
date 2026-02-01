# Connection Implementation Guide

This guide explains how the API Data Fetcher example implements IBM Watsonx Orchestrate connections following the official documentation patterns.

## Connection Pattern Overview

IBM Watsonx Orchestrate uses a three-step process for connection authentication:

1. **Declare** expected credentials in tool decorators
2. **Fetch** credentials at runtime using the connections API
3. **Use** credentials in API requests

## Step-by-Step Implementation

### 1. Import Required Modules

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections
import requests
from requests.auth import HTTPBasicAuth
```

### 2. Define Your App ID

```python
MY_APP_ID = 'basic-connection-app'
```

This should match the `app_id` in your connection YAML file.

### 3. Declare Expected Credentials

Use the `@tool` decorator with `expected_credentials`:

```python
@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def my_api_tool(endpoint: str) -> str:
    """Your tool documentation"""
    # Tool implementation here
    pass
```

**Available Connection Types:**
- `ConnectionType.BASIC_AUTH` - Basic authentication (username/password)
- `ConnectionType.API_KEY_AUTH` - API key authentication
- `ConnectionType.BEARER_AUTH` - Bearer token authentication
- `ConnectionType.OAUTH2_CLIENT_CREDS` - OAuth 2.0 client credentials
- `ConnectionType.OAUTH2_AUTH_CODE` - OAuth 2.0 authorization code
- `ConnectionType.OAUTH2_PASSWORD` - OAuth 2.0 password grant
- `ConnectionType.KEY_VALUE` - Key-value pairs

### 4. Fetch Credentials at Runtime

Inside your tool function, fetch the credentials:

```python
@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def fetch_data(endpoint: str) -> str:
    # Fetch credentials
    creds = connections.basic_auth(MY_APP_ID)
    
    # Access credential properties
    base_url = creds.url
    username = creds.username
    password = creds.password
    
    # Use credentials...
```

**Connection Methods by Type:**
- Basic Auth: `connections.basic_auth(app_id)` → `.url`, `.username`, `.password`
- API Key: `connections.api_key_auth(app_id)` → `.url`, `.api_key`
- Bearer: `connections.bearer_auth(app_id)` → `.url`, `.token`
- OAuth: `connections.oauth2_client_creds(app_id)` → `.url`, `.access_token`
- Key-Value: `connections.key_value(app_id)` → returns dict

### 5. Make Authenticated Requests

#### Basic Authentication Example

```python
@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def fetch_api_data(endpoint: str) -> str:
    # Get credentials
    creds = connections.basic_auth(MY_APP_ID)
    
    # Build URL
    url = f"{creds.url.rstrip('/')}{endpoint}"
    
    # Set headers
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Make authenticated request
    response = requests.get(
        url,
        headers=headers,
        auth=HTTPBasicAuth(creds.username, creds.password)
    )
    response.raise_for_status()
    
    return response.json()
```

## Multi-Connection Tools

You can declare multiple connections for a single tool:

```python
@tool(
    expected_credentials=[
        {"app_id": "my-app-1", "type": ConnectionType.BASIC_AUTH},
        {"app_id": "my-app-2", "type": ConnectionType.API_KEY_AUTH}
    ]
)
def multi_connection_tool():
    # Use first connection
    creds1 = connections.basic_auth("my-app-1")
    
    # Use second connection
    creds2 = connections.api_key_auth("my-app-2")
    
    # Use both...
```

## Multiple Connection Types for Same App

Support different auth methods in different environments:

```python
@tool(
    expected_credentials=[
        {
            "app_id": "my-app", 
            "type": [
                ConnectionType.BASIC_AUTH,
                ConnectionType.OAUTH2_CLIENT_CREDS
            ]
        }
    ]
)
def flexible_auth_tool():
    # Determine which connection type is active
    conn_type = connections.connection_type("my-app")
    
    if conn_type == ConnectionType.BASIC_AUTH:
        creds = connections.basic_auth("my-app")
        # Use basic auth
    elif conn_type == ConnectionType.OAUTH2_CLIENT_CREDS:
        creds = connections.oauth2_client_creds("my-app")
        # Use OAuth
    else:
        raise ValueError(f"Unexpected connection type: {conn_type}")
```

## Importing Tools with Connections

### Basic Import

```bash
orchestrate tools import -k python -f my_tools.py -a basic-connection-app
```

### Multiple Connections

```bash
orchestrate tools import -k python -f my_tools.py \
  -a app-1 \
  -a app-2
```

### Remapping Connection Names

If your code uses different names than Orchestrate:

```bash
orchestrate tools import -k python -f my_tools.py \
  -a app_id_in_code=app_id_in_orchestrate
```

## Local Testing

Test tools locally by setting environment variables:

```bash
# Set connection type
export WXO_SECURITY_SCHEMA_basic_connection_app=basic_auth

# Set connection fields
export WXO_CONNECTION_basic_connection_app_url=https://api.example.com
export WXO_CONNECTION_basic_connection_app_username=myuser
export WXO_CONNECTION_basic_connection_app_password=mypass

# Run your tool
python my_tools.py
```

**Important:** App IDs must be sanitized in environment variables (replace non-alphanumeric chars with `_`):
- `basic-connection-app` → `basic_connection_app`
- `my.app.id` → `my_app_id`

## Error Handling

Always handle connection and API errors gracefully:

```python
@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def robust_tool(endpoint: str) -> str:
    try:
        # Fetch credentials
        creds = connections.basic_auth(MY_APP_ID)
        
        # Make request
        response = requests.get(
            f"{creds.url}{endpoint}",
            auth=HTTPBasicAuth(creds.username, creds.password),
            timeout=30
        )
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        return {"error": f"HTTP error: {e}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Failed to connect to API"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
```

## Complete Working Example

Here's a complete, working tool implementation:

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections
import requests
from requests.auth import HTTPBasicAuth
import json

MY_APP_ID = 'basic-connection-app'

@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def get_user_data(user_id: str) -> str:
    """
    Fetch user data from an authenticated API.
    
    Args:
        user_id: The ID of the user to fetch
        
    Returns:
        JSON string with user data
    """
    try:
        # Get connection credentials
        creds = connections.basic_auth(MY_APP_ID)
        
        # Build the API URL
        url = f"{creds.url.rstrip('/')}/api/users/{user_id}"
        
        # Set headers
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Make authenticated request
        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth(creds.username, creds.password),
            timeout=30
        )
        
        # Raise exception for bad status codes
        response.raise_for_status()
        
        # Return the response
        return json.dumps(response.json(), indent=2)
        
    except requests.exceptions.RequestException as e:
        error_response = {
            "error": "API request failed",
            "details": str(e)
        }
        return json.dumps(error_response, indent=2)
```

## Best Practices

1. **Always declare expected_credentials** - Don't skip this or tools won't import correctly
2. **Handle errors gracefully** - APIs can fail, connection can be lost
3. **Use timeouts** - Prevent hanging requests
4. **Sanitize inputs** - Validate and clean user inputs before using in requests
5. **Don't expose credentials** - Never log or return credentials in responses
6. **Test locally first** - Use environment variables to test before deploying
7. **Document your tools** - Clear docstrings help users understand usage
8. **Use appropriate HTTP methods** - GET for reading, POST for creating, etc.

## Troubleshooting

### Tool Import Fails

**Error:** `Connection type does not match`

**Solution:** Ensure your `expected_credentials` type matches the actual connection type in Orchestrate.

### Runtime Connection Error

**Error:** `Cannot find connection 'my-app'`

**Solution:** 
1. Check connection is applied: `orchestrate connections list`
2. Ensure you used `-a` flag during import
3. Verify credentials are set

### Authentication Fails

**Error:** `401 Unauthorized`

**Solution:**
1. Verify credentials are correct
2. Check API endpoint URL is correct
3. Ensure connection type matches API requirements

## Reference

- [Official IBM Watsonx Orchestrate Connection Documentation](https://developer.watson-orchestrate.ibm.com/connections/associate_connection_to_tool/python_connections)
- [Managing Connections](https://developer.watson-orchestrate.ibm.com/connections/managing_connections)
- [Connection Types Reference](https://developer.watson-orchestrate.ibm.com/connections/connection_types)
