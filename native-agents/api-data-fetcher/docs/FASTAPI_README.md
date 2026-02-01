# FastAPI Backend Server

This directory includes a complete FastAPI backend server that provides authenticated API endpoints for the watsonx agents to consume.

## Overview

The FastAPI application demonstrates a real-world API with:
- **Basic Authentication** - Username/password protection
- **RESTful Endpoints** - Standard API design patterns
- **Mock Data** - Pre-populated users, products, and orders
- **Interactive Documentation** - Auto-generated API docs
- **CORS Support** - Cross-origin requests enabled

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
# Development mode with auto-reload
./run_server.sh start-dev

# Production mode
./run_server.sh start

# Background mode
./run_server.sh start-background
```

### 3. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Valid Credentials

The server has three built-in test accounts:

| Username | Password   | Description      |
|----------|------------|------------------|
| `demo`   | `demo123`  | Demo account     |
| `admin`  | `admin123` | Admin account    |
| `user`   | `password` | Standard user    |

## API Endpoints

### Public Endpoints (No Auth Required)

- `GET /` - API information
- `GET /health` - Health check

### Protected Endpoints (Basic Auth Required)

#### Data Endpoints
- `GET /api/v1/data` - Get general data
- `GET /api/v1/products` - List all products
  - Query params: `status`, `category`
- `GET /api/v1/orders` - List all orders
- `GET /api/v1/dashboard` - Get dashboard metrics
- `GET /api/v1/metrics` - Get system metrics

#### User Endpoints
- `GET /api/v1/users` - List all users
  - Query params: `status`, `department`
- `GET /api/v1/users/{user_id}` - Get specific user info
- `POST /api/v1/users` - Create a new user (demo)

#### Search Endpoint
- `GET /api/v1/search` - Search data
  - Query params: `q` (required), `filters` (optional JSON)

## Testing the API

### Using curl

```bash
# Test health endpoint (no auth)
curl http://localhost:8000/health

# Test with authentication
curl -u demo:demo123 http://localhost:8000/api/v1/data

# Get user info
curl -u demo:demo123 http://localhost:8000/api/v1/users/123

# Search with filters
curl -u demo:demo123 "http://localhost:8000/api/v1/search?q=laptop&filters=%7B%22status%22%3A%22active%22%7D"
```

### Using the Management Script

```bash
# Check if server is running
./run_server.sh status

# Test authentication
./run_server.sh test-auth

# View logs (if running in background)
./run_server.sh logs

# Stop server
./run_server.sh stop
```

### Using the Interactive Docs

1. Navigate to http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Enter credentials when prompted:
   - Username: `demo`
   - Password: `demo123`
5. Execute the request

## Configuring Watsonx Orchestrate

### 1. Update Connection Configuration

Edit `../../connections/basic-connections.yml`:

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

### 2. Apply the Connection

```bash
cd ../../connections
orchestrate connections apply -f basic-connections.yml
```

### 3. Set Credentials

```bash
orchestrate connections set-credentials -a basic-connection-app \
  --env draft \
  -u demo \
  -p demo123
```

### 4. Import and Deploy Agents

```bash
cd ../native-agents/api-data-fetcher
./manage_api_fetcher.sh import-all
./manage_api_fetcher.sh deploy-all
```

## Server Management Commands

The `run_server.sh` script provides several commands:

```bash
# Start server in foreground
./run_server.sh start

# Start with auto-reload (for development)
./run_server.sh start-dev

# Start in background
./run_server.sh start-background

# Check status
./run_server.sh status

# Test authentication
./run_server.sh test-auth

# View logs
./run_server.sh logs

# Stop server
./run_server.sh stop
```

## Mock Data

The server includes pre-populated mock data:

### Users (3 users)
- User IDs: `123`, `456`, `789`
- Different departments, roles, and statuses

### Products (5 products)
- Categories: electronics, furniture, lighting
- Various prices and stock levels
- Active and inactive items

### Orders (2 orders)
- Different statuses (completed, pending)
- Linked to users

## API Response Format

All authenticated endpoints return responses in this format:

```json
{
  "success": true,
  "authenticated_as": "demo",
  "data": {
    // ... response data
  }
}
```

Error responses:

```json
{
  "error": "Error message",
  "status_code": 401
}
```

## Example Requests & Responses

### Get User Info

**Request:**
```bash
curl -u demo:demo123 http://localhost:8000/api/v1/users/123
```

**Response:**
```json
{
  "success": true,
  "authenticated_as": "demo",
  "user": {
    "id": "123",
    "username": "user_123",
    "email": "user_123@example.com",
    "first_name": "Alice",
    "last_name": "Johnson",
    "status": "active",
    "roles": ["user", "editor"],
    "metadata": {
      "department": "Engineering",
      "location": "San Francisco"
    }
  }
}
```

### Search with Filters

**Request:**
```bash
curl -u demo:demo123 "http://localhost:8000/api/v1/search?q=laptop&filters=%7B%22status%22:%22active%22%7D"
```

**Response:**
```json
{
  "success": true,
  "authenticated_as": "demo",
  "query": "laptop",
  "filters": {"status": "active"},
  "results": [
    {
      "id": "prod_1",
      "title": "Laptop Pro 15",
      "description": "High-performance laptop for professionals",
      "relevance_score": 0.95,
      "category": "electronics",
      "url": "/api/v1/products/1"
    }
  ],
  "total_results": 1
}
```

## Development Tips

### Adding New Endpoints

1. Add your endpoint function to `fastapi_app.py`:
   ```python
   @app.get("/api/v1/my-endpoint")
   async def my_endpoint(username: str = Depends(verify_credentials)):
       return {"success": True, "data": "..."}
   ```

2. Restart the server to see changes (auto-reload in dev mode)

### Adding New Mock Data

Edit the `MOCK_*` dictionaries at the top of `fastapi_app.py`:

```python
MOCK_PRODUCTS = [
    {
        "id": 6,
        "name": "New Product",
        "category": "electronics",
        "status": "active",
        # ... more fields
    }
]
```

### Changing Port

Edit `run_server.sh` and change the `PORT` variable:

```bash
PORT=8080  # Change from 8000 to 8080
```

## Production Considerations

For production deployment, consider:

1. **Secure Credentials**: Use a proper user database instead of hardcoded credentials
2. **HTTPS**: Use SSL/TLS certificates
3. **Database**: Replace mock data with a real database (PostgreSQL, MongoDB, etc.)
4. **Authentication**: Consider OAuth2, JWT tokens, or API keys
5. **Rate Limiting**: Add rate limiting middleware
6. **Logging**: Implement structured logging
7. **Monitoring**: Add health checks and metrics
8. **Environment Variables**: Use `.env` files for configuration

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Stop the server
./run_server.sh stop

# Or kill the process manually
kill <PID>
```

### Server Won't Start

1. Check if dependencies are installed: `pip install -r requirements.txt`
2. Check the log file: `cat fastapi.log`
3. Try running manually: `python fastapi_app.py`

### Authentication Fails

1. Verify you're using correct credentials
2. Check the server logs for authentication attempts
3. Test with: `./run_server.sh test-auth`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [HTTP Basic Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication)
- [REST API Best Practices](https://restfulapi.net/)
