"""
FastAPI Backend Application for API Data Fetcher Example
This app provides authenticated API endpoints for the watsonx agents to consume.
Supports multiple authentication methods: Basic Auth, Bearer Token, API Key, and Key-Value headers.
"""
from fastapi import FastAPI, HTTPException, Depends, Query, status, Header, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union
import secrets
from datetime import datetime
from enum import Enum

# Initialize FastAPI app
app = FastAPI(
    title="API Data Fetcher Backend",
    description="Demo API with multiple authentication methods for IBM Watsonx Orchestrate agents",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication schemes
basic_security = HTTPBasic()
bearer_security = HTTPBearer()

# Authentication type enum
class AuthType(str, Enum):
    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "api_key"
    KEY_VALUE = "key_value"

# Mock credentials for different auth types (in production, use a proper database)
VALID_BASIC_CREDENTIALS = {
    "admin": "admin123",
    "user": "password",
    "demo": "demo123"
}

VALID_BEARER_TOKENS = {
    "token123abc",
    "demo-token-456",
    "test-bearer-token"
}

VALID_API_KEYS = {
    "api-key-12345",
    "demo-api-key",
    "test-key-xyz"
}

VALID_KEY_VALUE_PAIRS = {
    "client-id": ["client-123", "client-456"],
    "x-api-token": ["secret-token-1", "secret-token-2"]
}

# Mock database
MOCK_USERS = {
    "123": {
        "id": "123",
        "username": "user_123",
        "email": "user_123@example.com",
        "first_name": "Alice",
        "last_name": "Johnson",
        "status": "active",
        "created_at": "2024-01-15T10:30:00Z",
        "last_login": "2026-02-01T14:22:00Z",
        "roles": ["user", "editor"],
        "metadata": {
            "department": "Engineering",
            "location": "San Francisco"
        }
    },
    "456": {
        "id": "456",
        "username": "user_456",
        "email": "user_456@example.com",
        "first_name": "Bob",
        "last_name": "Smith",
        "status": "active",
        "created_at": "2024-03-20T09:15:00Z",
        "last_login": "2026-01-30T11:45:00Z",
        "roles": ["user", "admin"],
        "metadata": {
            "department": "Marketing",
            "location": "New York"
        }
    },
    "789": {
        "id": "789",
        "username": "user_789",
        "email": "user_789@example.com",
        "first_name": "Carol",
        "last_name": "Williams",
        "status": "inactive",
        "created_at": "2023-12-10T14:20:00Z",
        "last_login": "2025-11-15T16:30:00Z",
        "roles": ["user"],
        "metadata": {
            "department": "Sales",
            "location": "Boston"
        }
    }
}

MOCK_PRODUCTS = [
    {
        "id": 1,
        "name": "Laptop Pro 15",
        "category": "electronics",
        "status": "active",
        "price": 1299.99,
        "stock": 45,
        "description": "High-performance laptop for professionals"
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "category": "electronics",
        "status": "active",
        "price": 29.99,
        "stock": 150,
        "description": "Ergonomic wireless mouse"
    },
    {
        "id": 3,
        "name": "Office Chair Deluxe",
        "category": "furniture",
        "status": "active",
        "price": 449.99,
        "stock": 30,
        "description": "Comfortable ergonomic office chair"
    },
    {
        "id": 4,
        "name": "Desk Lamp LED",
        "category": "lighting",
        "status": "inactive",
        "price": 39.99,
        "stock": 0,
        "description": "Energy-efficient LED desk lamp"
    },
    {
        "id": 5,
        "name": "USB-C Hub",
        "category": "electronics",
        "status": "active",
        "price": 59.99,
        "stock": 75,
        "description": "Multi-port USB-C hub with charging"
    }
]

MOCK_ORDERS = [
    {
        "id": "ORD-001",
        "user_id": "123",
        "status": "completed",
        "total": 1329.98,
        "items": [1, 2],
        "created_at": "2026-01-15T10:00:00Z"
    },
    {
        "id": "ORD-002",
        "user_id": "456",
        "status": "pending",
        "total": 449.99,
        "items": [3],
        "created_at": "2026-01-20T14:30:00Z"
    },
    {
        "id": "ORD-003",
        "user_id": "123",
        "status": "shipped",
        "total": 59.99,
        "items": [5],
        "created_at": "2026-01-25T09:00:00Z"
    }
]

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    department: Optional[str] = None

# Authentication functions

def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(basic_security)) -> Dict[str, str]:
    """Verify basic authentication credentials"""
    username = credentials.username
    password = credentials.password
    
    if username not in VALID_BASIC_CREDENTIALS or not secrets.compare_digest(
        password.encode("utf8"),
        VALID_BASIC_CREDENTIALS[username].encode("utf8")
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid basic auth credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return {"auth_type": AuthType.BASIC, "user": username}

def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_security)) -> Dict[str, str]:
    """Verify bearer token authentication"""
    token = credentials.credentials
    
    if token not in VALID_BEARER_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"auth_type": AuthType.BEARER, "token": token}

def verify_api_key(x_api_key: Optional[str] = Header(None)) -> Dict[str, str]:
    """Verify API key authentication via header"""
    if not x_api_key or x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return {"auth_type": AuthType.API_KEY, "api_key": x_api_key}

def verify_key_value(
    x_client_id: Optional[str] = Header(None),
    x_api_token: Optional[str] = Header(None)
) -> Dict[str, str]:
    """Verify key-value pair authentication via custom headers"""
    if x_client_id and x_client_id in VALID_KEY_VALUE_PAIRS.get("client-id", []):
        return {"auth_type": AuthType.KEY_VALUE, "client_id": x_client_id}
    
    if x_api_token and x_api_token in VALID_KEY_VALUE_PAIRS.get("x-api-token", []):
        return {"auth_type": AuthType.KEY_VALUE, "api_token": x_api_token}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing key-value authentication headers",
    )

def verify_any_auth(
    request: Request,
    x_api_key: Optional[str] = Header(None),
    x_client_id: Optional[str] = Header(None),
    x_api_token: Optional[str] = Header(None),
    authorization: Optional[str] = Header(None)
) -> Dict[str, Any]:
    """
    Flexible authentication that accepts any valid auth method.
    Tries different auth methods in order: Basic, Bearer, API Key, Key-Value
    """
    # Try Basic Auth
    if authorization and authorization.startswith("Basic "):
        try:
            import base64
            credentials = base64.b64decode(authorization.split(" ")[1]).decode("utf-8")
            username, password = credentials.split(":", 1)
            
            if username in VALID_BASIC_CREDENTIALS and secrets.compare_digest(
                password.encode("utf8"),
                VALID_BASIC_CREDENTIALS[username].encode("utf8")
            ):
                return {"auth_type": AuthType.BASIC, "user": username}
        except Exception:
            pass
    
    # Try Bearer Token
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        if token in VALID_BEARER_TOKENS:
            return {"auth_type": AuthType.BEARER, "token": token}
    
    # Try API Key
    if x_api_key and x_api_key in VALID_API_KEYS:
        return {"auth_type": AuthType.API_KEY, "api_key": x_api_key}
    
    # Try Key-Value
    if x_client_id and x_client_id in VALID_KEY_VALUE_PAIRS.get("client-id", []):
        return {"auth_type": AuthType.KEY_VALUE, "client_id": x_client_id}
    
    if x_api_token and x_api_token in VALID_KEY_VALUE_PAIRS.get("x-api-token", []):
        return {"auth_type": AuthType.KEY_VALUE, "api_token": x_api_token}
    
    # No valid authentication found
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Supported methods: Basic Auth, Bearer Token, API Key (x-api-key), or Key-Value (x-client-id or x-api-token)",
        headers={"WWW-Authenticate": "Basic, Bearer, ApiKey"},
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": "API Data Fetcher Backend - Multi-Auth Support",
        "version": "2.0.0",
        "authentication": {
            "supported_methods": ["Basic Auth", "Bearer Token", "API Key", "Key-Value Headers"],
            "note": "Most endpoints accept any valid authentication method"
        },
        "docs": "/docs",
        "test_credentials": {
            "basic_auth": {
                "username": "demo",
                "password": "demo123"
            },
            "bearer_token": "demo-token-456",
            "api_key": "demo-api-key",
            "key_value": {
                "x-client-id": "client-123",
                "x-api-token": "secret-token-1"
            }
        }
    }

# Health check endpoint (no auth required)
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

# API v1 endpoints with flexible authentication

@app.get("/api/v1/data")
async def get_data(auth: Dict[str, Any] = Depends(verify_any_auth)):
    """Get general data - accepts any valid authentication method"""
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "data": {
            "items": MOCK_PRODUCTS[:3],
            "total": len(MOCK_PRODUCTS[:3])
        }
    }

@app.get("/api/v1/products")
async def get_products(
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    auth: Dict[str, Any] = Depends(verify_any_auth)
):
    """Get all products with optional filters - accepts any valid authentication"""
    products = MOCK_PRODUCTS.copy()
    
    # Apply filters
    if status:
        products = [p for p in products if p["status"] == status]
    if category:
        products = [p for p in products if p["category"] == category]
    
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "data": {
            "items": products,
            "total": len(products)
        }
    }

@app.get("/api/v1/orders")
async def get_orders(auth: Dict[str, Any] = Depends(verify_any_auth)):
    """Get all orders - accepts any valid authentication"""
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "data": {
            "items": MOCK_ORDERS,
            "total": len(MOCK_ORDERS)
        }
    }

@app.get("/api/v1/users/{user_id}")
async def get_user(
    user_id: str,
    auth: Dict[str, Any] = Depends(verify_any_auth)
):
    """Get user information by ID - accepts any valid authentication"""
    if user_id not in MOCK_USERS:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID '{user_id}' not found"
        )
    
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "data": MOCK_USERS[user_id]
    }

@app.get("/api/v1/users")
async def list_users(
    status: Optional[str] = Query(None, description="Filter by status"),
    department: Optional[str] = Query(None, description="Filter by department"),
    auth: Dict[str, Any] = Depends(verify_any_auth)
):
    """List all users with optional filters - accepts any valid authentication"""
    users = list(MOCK_USERS.values())
    
    # Apply filters
    if status:
        users = [u for u in users if u["status"] == status]
    if department:
        users = [u for u in users if u["metadata"].get("department") == department]
    
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "data": {
            "users": users,
            "total": len(users)
        }
    }

@app.get("/api/v1/search")
async def search_data(
    q: str = Query(..., description="Search query"),
    filters: Optional[str] = Query(None, description="JSON filters"),
    auth: Dict[str, Any] = Depends(verify_any_auth)
):
    """Search for data with query and optional filters - accepts any valid authentication"""
    import json
    
    # Parse filters if provided
    filter_dict = {}
    if filters:
        try:
            filter_dict = json.loads(filters)
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON in filters parameter"
            )
    
    # Simple search implementation
    results = []
    
    # Search in products
    for product in MOCK_PRODUCTS:
        if q.lower() in product["name"].lower() or q.lower() in product["description"].lower():
            # Apply filters if specified
            if filter_dict:
                if "status" in filter_dict and product["status"] != filter_dict["status"]:
                    continue
                if "category" in filter_dict and product["category"] != filter_dict["category"]:
                    continue
            
            results.append({
                "id": f"prod_{product['id']}",
                "title": product["name"],
                "description": product["description"],
                "relevance_score": 0.95 if q.lower() in product["name"].lower() else 0.75,
                "category": product["category"],
                "url": f"/api/v1/products/{product['id']}"
            })
    
    # Search in users
    for user in MOCK_USERS.values():
        if q.lower() in user["username"].lower() or q.lower() in user["email"].lower():
            if filter_dict and "status" in filter_dict and user["status"] != filter_dict["status"]:
                continue
            
            results.append({
                "id": f"user_{user['id']}",
                "title": f"{user['first_name']} {user['last_name']}",
                "description": f"User: {user['username']} - {user['metadata']['department']}",
                "relevance_score": 0.85,
                "category": "users",
                "url": f"/api/v1/users/{user['id']}"
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "data": {
            "results": results,
            "total_results": len(results),
            "page": 1,
            "per_page": 10
        }
    }

@app.get("/api/v1/dashboard")
async def get_dashboard(auth: Dict[str, Any] = Depends(verify_any_auth)):
    """Get dashboard metrics - accepts any valid authentication"""
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "data": {
            "metrics": {
                "total_users": len(MOCK_USERS),
                "active_users": sum(1 for u in MOCK_USERS.values() if u["status"] == "active"),
                "total_products": len(MOCK_PRODUCTS),
                "active_products": sum(1 for p in MOCK_PRODUCTS if p["status"] == "active"),
                "total_orders": len(MOCK_ORDERS),
                "pending_orders": sum(1 for o in MOCK_ORDERS if o["status"] == "pending"),
                "completed_orders": sum(1 for o in MOCK_ORDERS if o["status"] == "completed"),
                "total_revenue": sum(o["total"] for o in MOCK_ORDERS)
            }
        }
    }

@app.get("/api/v1/metrics")
async def get_metrics(auth: Dict[str, Any] = Depends(verify_any_auth)):
    """Get system metrics - accepts any valid authentication"""
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "data": {
            "metrics": {
                "api_version": "2.0.0",
                "total_users": len(MOCK_USERS),
                "total_products": len(MOCK_PRODUCTS),
                "total_orders": len(MOCK_ORDERS),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
    }

@app.post("/api/v1/users")
async def create_user(
    user_data: UserCreate,
    auth: Dict[str, Any] = Depends(verify_any_auth)
):
    """Create a new user (demo endpoint) - accepts any valid authentication"""
    return {
        "success": True,
        "auth_method": auth.get("auth_type"),
        "message": "User created successfully (demo)",
        "data": user_data.dict()
    }

# Specific authentication method endpoints (for testing each type)

@app.get("/api/v1/auth/basic-only")
async def basic_auth_only(auth: Dict[str, str] = Depends(verify_basic_auth)):
    """Endpoint that only accepts basic authentication"""
    return {
        "success": True,
        "auth_method": "basic",
        "message": "Successfully authenticated with basic auth",
        "user": auth.get("user")
    }

@app.get("/api/v1/auth/bearer-only")
async def bearer_auth_only(auth: Dict[str, str] = Depends(verify_bearer_token)):
    """Endpoint that only accepts bearer token authentication"""
    return {
        "success": True,
        "auth_method": "bearer",
        "message": "Successfully authenticated with bearer token",
        "token": auth.get("token")[:10] + "..."
    }

@app.get("/api/v1/auth/apikey-only")
async def apikey_auth_only(auth: Dict[str, str] = Depends(verify_api_key)):
    """Endpoint that only accepts API key authentication"""
    return {
        "success": True,
        "auth_method": "api_key",
        "message": "Successfully authenticated with API key",
        "api_key": auth.get("api_key")[:10] + "..."
    }

@app.get("/api/v1/auth/keyvalue-only")
async def keyvalue_auth_only(auth: Dict[str, str] = Depends(verify_key_value)):
    """Endpoint that only accepts key-value authentication"""
    return {
        "success": True,
        "auth_method": "key_value",
        "message": "Successfully authenticated with key-value headers",
        "credentials": {k: v for k, v in auth.items() if k != "auth_type"}
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)