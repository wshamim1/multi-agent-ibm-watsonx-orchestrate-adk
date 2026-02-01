# Multi-Authentication Guide

The FastAPI backend now supports **4 different authentication methods**, making it easy to test different connection types with IBM Watsonx Orchestrate.

## Supported Authentication Methods

1. **Basic Authentication** (username/password)
2. **Bearer Token** (JWT-style tokens)
3. **API Key** (via x-api-key header)
4. **Key-Value** (custom headers like x-client-id)

## Test Credentials

### Basic Auth
```bash
Username: demo
Password: demo123

Username: admin
Password: admin123

Username: user
Password: password
```

### Bearer Tokens
```bash
demo-token-456
token123abc
test-bearer-token
```

### API Keys
```bash
demo-api-key
api-key-12345
test-key-xyz
```

### Key-Value Headers
```bash
x-client-id: client-123
x-client-id: client-456

x-api-token: secret-token-1
x-api-token: secret-token-2
```

## Using Each Authentication Method

### 1. Basic Authentication

**curl:**
```bash
curl -u demo:demo123 http://localhost:8000/api/v1/data
```

**Python (requests):**
```python
from requests.auth import HTTPBasicAuth
response = requests.get(
    "http://localhost:8000/api/v1/data",
    auth=HTTPBasicAuth("demo", "demo123")
)
```

**Watsonx Tool:**
```python
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections

@tool(
    expected_credentials=[
        {"app_id": "my-app", "type": ConnectionType.BASIC_AUTH}
    ]
)
def my_tool():
    creds = connections.basic_auth("my-app")
    response = requests.get(
        url,
        auth=HTTPBasicAuth(creds.username, creds.password)
    )
```

### 2. Bearer Token

**curl:**
```bash
curl -H "Authorization: Bearer demo-token-456" \
  http://localhost:8000/api/v1/data
```

**Python (requests):**
```python
headers = {"Authorization": "Bearer demo-token-456"}
response = requests.get(
    "http://localhost:8000/api/v1/data",
    headers=headers
)
```

**Watsonx Tool:**
```python
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections

@tool(
    expected_credentials=[
        {"app_id": "my-app", "type": ConnectionType.BEARER_AUTH}
    ]
)
def my_tool():
    creds = connections.bearer_auth("my-app")
    headers = {"Authorization": f"Bearer {creds.token}"}
    response = requests.get(url, headers=headers)
```

### 3. API Key

**curl:**
```bash
curl -H "x-api-key: demo-api-key" \
  http://localhost:8000/api/v1/data
```

**Python (requests):**
```python
headers = {"x-api-key": "demo-api-key"}
response = requests.get(
    "http://localhost:8000/api/v1/data",
    headers=headers
)
```

**Watsonx Tool:**
```python
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections

@tool(
    expected_credentials=[
        {"app_id": "my-app", "type": ConnectionType.API_KEY_AUTH}
    ]
)
def my_tool():
    creds = connections.api_key_auth("my-app")
    headers = {"x-api-key": creds.api_key}
    response = requests.get(url, headers=headers)
```

### 4. Key-Value Headers

**curl:**
```bash
curl -H "x-client-id: client-123" \
  http://localhost:8000/api/v1/data

# Or with different header
curl -H "x-api-token: secret-token-1" \
  http://localhost:8000/api/v1/data
```

**Python (requests):**
```python
headers = {"x-client-id": "client-123"}
response = requests.get(
    "http://localhost:8000/api/v1/data",
    headers=headers
)
```

**Watsonx Tool:**
```python
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections

@tool(
    expected_credentials=[
        {"app_id": "my-app", "type": ConnectionType.KEY_VALUE}
    ]
)
def my_tool():
    creds = connections.key_value("my-app")
    headers = {"x-client-id": creds["client-id"]}
    response = requests.get(url, headers=headers)
```

## API Endpoints

### Flexible Auth Endpoints (Accept Any Method)

These endpoints accept **any valid authentication method**:

- `GET /api/v1/data`
- `GET /api/v1/products`
- `GET /api/v1/orders`
- `GET /api/v1/users`
- `GET /api/v1/users/{id}`
- `GET /api/v1/search`
- `GET /api/v1/dashboard`
- `GET /api/v1/metrics`

### Specific Auth Endpoints (Testing Only)

These endpoints only accept **one specific method**:

- `GET /api/v1/auth/basic-only` - Basic Auth only
- `GET /api/v1/auth/bearer-only` - Bearer Token only
- `GET /api/v1/auth/apikey-only` - API Key only
- `GET /api/v1/auth/keyvalue-only` - Key-Value only

## Testing All Methods

### Using the Test Script

```bash
cd backend
python test_multi_auth.py
```

This will test all authentication methods against all endpoints.

### Manual Testing

Test each method manually:

```bash
# Basic Auth
curl -u demo:demo123 http://localhost:8000/api/v1/data

# Bearer Token
curl -H "Authorization: Bearer demo-token-456" \
  http://localhost:8000/api/v1/data

# API Key
curl -H "x-api-key: demo-api-key" \
  http://localhost:8000/api/v1/data

# Key-Value
curl -H "x-client-id: client-123" \
  http://localhost:8000/api/v1/data
```

## Connection Configuration Examples

### For Basic Auth

`connections/basic-connections.yml`:
```yaml
spec_version: v1
kind: connection
app_id: basic-connection-app
environments:
    draft:
        kind: basic
        type: team
        server_url: http://localhost:8000
```

Set credentials:
```bash
orchestrate connections set-credentials -a basic-connection-app \
  --env draft \
  -u demo \
  -p demo123
```

### For Bearer Token

`connections/bearer-connections.yml`:
```yaml
spec_version: v1
kind: connection
app_id: bearer-connection-app
environments:
    draft:
        kind: bearer
        type: team
        server_url: http://localhost:8000
```

Set credentials:
```bash
orchestrate connections set-credentials -a bearer-connection-app \
  --env draft \
  --token demo-token-456
```

### For API Key

`connections/api-key-connections.yml`:
```yaml
spec_version: v1
kind: connection
app_id: api-key-connection-app
environments:
    draft:
        kind: api-key
        type: team
        server_url: http://localhost:8000
```

Set credentials:
```bash
orchestrate connections set-credentials -a api-key-connection-app \
  --env draft \
  --api-key demo-api-key
```

### For Key-Value

`connections/key-value-connections.yml`:
```yaml
spec_version: v1
kind: connection
app_id: key-value-connection-app
environments:
    draft:
        kind: key-value
        type: team
        server_url: http://localhost:8000
```

Set credentials:
```bash
orchestrate connections set-credentials -a key-value-connection-app \
  --env draft \
  --key client-id \
  --value client-123
```

## Response Format

All authenticated endpoints return:

```json
{
  "success": true,
  "auth_method": "basic" | "bearer" | "api_key" | "key_value",
  "data": {
    // ... response data
  }
}
```

The `auth_method` field indicates which authentication method was used.

## Error Responses

### 401 Unauthorized

When authentication fails:

```json
{
  "detail": "Authentication required. Supported methods: Basic Auth, Bearer Token, API Key (x-api-key), or Key-Value (x-client-id or x-api-token)"
}
```

### Common Issues

1. **No authentication provided**: Missing headers or credentials
2. **Wrong credentials**: Invalid username/password, token, or key
3. **Wrong header name**: Using incorrect header (e.g., `Authorization` instead of `x-api-key`)

## Interactive API Docs

Visit http://localhost:8000/docs to:
- See all available endpoints
- Try different authentication methods
- View request/response schemas
- Test API calls directly in the browser

## Best Practices

1. **Use appropriate auth for your use case**:
   - Basic Auth: Simple username/password
   - Bearer Token: Temporary access tokens
   - API Key: Long-lived API access
   - Key-Value: Custom authentication schemes

2. **Never hardcode credentials** in your code

3. **Use environment variables** or Orchestrate connections for credentials

4. **Test locally first** before deploying to production

5. **Rotate credentials regularly** in production systems

## Examples in Tools

See the updated tools in [`../tools/data_fetcher_tools.py`](../tools/data_fetcher_tools.py) for complete examples of using different authentication methods with IBM Watsonx Orchestrate.

## Troubleshooting

### Authentication Not Working

1. Check server is running: `./run_server.sh status`
2. Verify credentials match the test credentials above
3. Check headers are correctly formatted
4. Review server logs: `./run_server.sh logs`

### Wrong Auth Method

Some endpoints require specific methods. Check the endpoint documentation or use the flexible endpoints that accept any method.

### Connection Issues

Make sure the connection `server_url` points to the correct address (usually `http://localhost:8000` for local testing).
