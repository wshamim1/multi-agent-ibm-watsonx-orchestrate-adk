"""
API Data Fetcher Tools for IBM watsonx Orchestrate ADK
These tools demonstrate using basic authentication connections to fetch data from external APIs.
"""
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionType
from ibm_watsonx_orchestrate.run import connections
import json
import requests
from requests.auth import HTTPBasicAuth

MY_APP_ID = 'basic-connection-app'

@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def fetch_api_data(endpoint: str, method: str = "GET") -> str:
    """
    Fetch data from an API endpoint using basic authentication.
    
    This tool uses the basic-connection-app connection which provides
    authenticated access to the API using username/password credentials.
    
    Args:
        endpoint: The API endpoint path (e.g., "/api/v1/data")
        method: HTTP method to use (default: "GET")
        
    Returns:
        JSON string containing the API response data
        
    Examples:
        fetch_api_data("/api/v1/users")
        fetch_api_data("/api/v1/products", "GET")
    """
    # Fetch connection credentials
    creds = connections.basic_auth(MY_APP_ID)
    base_url = creds.url
    
    # Construct full URL
    url = f"{base_url.rstrip('/')}{endpoint}"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        # Make authenticated request using basic auth credentials
        if method.upper() == "GET":
            response = requests.get(
                url,
                headers=headers,
                auth=HTTPBasicAuth(creds.username, creds.password)
            )
        elif method.upper() == "POST":
            response = requests.post(
                url,
                headers=headers,
                json={},
                auth=HTTPBasicAuth(creds.username, creds.password)
            )
        else:
            return json.dumps({"error": f"Unsupported HTTP method: {method}"})
        
        response.raise_for_status()
        
        # Return the actual API response
        return json.dumps(response.json(), indent=2)
        
    except requests.exceptions.RequestException as e:
        # If actual API call fails, return mock data for demonstration
        response_data = {
            "success": True,
            "endpoint": endpoint,
            "method": method,
            "message": "Mock data returned (API endpoint not reachable)",
            "note": f"Using credentials for {creds.username} at {base_url}",
            "data": {
                "items": [
                    {"id": 1, "name": "Item 1", "status": "active"},
                    {"id": 2, "name": "Item 2", "status": "active"},
                    {"id": 3, "name": "Item 3", "status": "inactive"}
                ],
                "total": 3
            }
        }
        return json.dumps(response_data, indent=2)


@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def fetch_user_info(user_id: str) -> str:
    """
    Retrieve user information from the API using basic authentication.
    
    This tool demonstrates fetching specific user data from an authenticated API endpoint.
    
    Args:
        user_id: The unique identifier of the user to retrieve
        
    Returns:
        JSON string containing user information
        
    Examples:
        fetch_user_info("123")
        fetch_user_info("user_456")
    """
    # Fetch connection credentials
    creds = connections.basic_auth(MY_APP_ID)
    base_url = creds.url
    
    # Construct API endpoint URL
    url = f"{base_url.rstrip('/')}/api/v1/users/{user_id}"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        # Make authenticated GET request
        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth(creds.username, creds.password)
        )
        response.raise_for_status()
        
        # Return the actual API response
        return json.dumps(response.json(), indent=2)
        
    except requests.exceptions.RequestException as e:
        # If actual API call fails, return mock data for demonstration
        user_data = {
            "success": True,
            "message": "Mock data returned (API endpoint not reachable)",
            "authenticated_as": creds.username,
            "user": {
                "id": user_id,
                "username": f"user_{user_id}",
                "email": f"user_{user_id}@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "status": "active",
                "created_at": "2024-01-15T10:30:00Z",
                "last_login": "2026-01-31T14:22:00Z",
                "roles": ["user", "editor"],
                "metadata": {
                    "department": "Engineering",
                    "location": "San Francisco"
                }
            }
        }
        return json.dumps(user_data, indent=2)


@tool(
    expected_credentials=[
        {"app_id": MY_APP_ID, "type": ConnectionType.BASIC_AUTH}
    ]
)
def search_api_data(query: str, filters: str = "") -> str:
    """
    Search for data in the API using query parameters and basic authentication.
    
    This tool demonstrates performing searches against an authenticated API endpoint
    with optional filters.
    
    Args:
        query: The search query string
        filters: Optional filters in JSON format (e.g., '{"status": "active", "type": "premium"}')
        
    Returns:
        JSON string containing search results
        
    Examples:
        search_api_data("product")
        search_api_data("customer", '{"status": "active"}')
    """
    # Fetch connection credentials
    creds = connections.basic_auth(MY_APP_ID)
    base_url = creds.url
    
    # Parse filters if provided
    filter_dict = {}
    if filters:
        try:
            filter_dict = json.loads(filters)
        except json.JSONDecodeError:
            filter_dict = {}
    
    # Construct API endpoint URL with query parameters
    url = f"{base_url.rstrip('/')}/api/v1/search"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Build query parameters
    params = {'q': query}
    if filter_dict:
        params['filters'] = json.dumps(filter_dict)
    
    try:
        # Make authenticated GET request with query parameters
        response = requests.get(
            url,
            headers=headers,
            params=params,
            auth=HTTPBasicAuth(creds.username, creds.password)
        )
        response.raise_for_status()
        
        # Return the actual API response
        return json.dumps(response.json(), indent=2)
        
    except requests.exceptions.RequestException as e:
        # If actual API call fails, return mock data for demonstration
        search_results = {
            "success": True,
            "message": "Mock data returned (API endpoint not reachable)",
            "authenticated_as": creds.username,
            "query": query,
            "filters": filter_dict,
            "results": [
                {
                    "id": "result_1",
                    "title": f"Result matching '{query}'",
                    "description": "This is a search result that matches your query",
                    "relevance_score": 0.95,
                    "category": "products",
                    "url": "/api/v1/items/result_1"
                },
                {
                    "id": "result_2",
                    "title": f"Another match for '{query}'",
                    "description": "Secondary result matching the search criteria",
                    "relevance_score": 0.87,
                    "category": "services",
                    "url": "/api/v1/items/result_2"
                }
            ],
            "total_results": 2,
            "page": 1,
            "per_page": 10
        }
        return json.dumps(search_results, indent=2)


@tool
def process_api_response(raw_data: str) -> str:
    """
    Process and analyze raw API response data.
    
    This tool takes raw JSON data from API responses and extracts
    key insights and summaries.
    
    Args:
        raw_data: Raw JSON string from API response
        
    Returns:
        Processed and summarized data
        
    Examples:
        process_api_response('{"items": [...], "total": 3}')
    """
    try:
        data = json.loads(raw_data)
        
        # Extract key information
        summary = {
            "processed": True,
            "summary": "Data processing complete"
        }
        
        # Check for common data patterns
        if "items" in data.get("data", {}):
            items = data["data"]["items"]
            summary["total_items"] = len(items)
            summary["active_items"] = sum(1 for item in items if item.get("status") == "active")
            summary["inactive_items"] = sum(1 for item in items if item.get("status") == "inactive")
            
        if "user" in data:
            user = data["user"]
            summary["user_summary"] = {
                "username": user.get("username"),
                "status": user.get("status"),
                "roles": user.get("roles", [])
            }
            
        if "results" in data:
            results = data["results"]
            summary["search_summary"] = {
                "total_results": len(results),
                "avg_relevance": sum(r.get("relevance_score", 0) for r in results) / len(results) if results else 0,
                "categories": list(set(r.get("category") for r in results))
            }
        
        return json.dumps(summary, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Failed to process data: {str(e)}"})


@tool
def format_data_report(data: str, format_type: str = "summary") -> str:
    """
    Format processed data into a human-readable report.
    
    Args:
        data: JSON string containing processed data
        format_type: Type of report format ("summary", "detailed", "table")
        
    Returns:
        Formatted report string
        
    Examples:
        format_data_report('{"total_items": 3}', "summary")
        format_data_report('{"user_summary": {...}}', "detailed")
    """
    try:
        data_dict = json.loads(data)
        
        if format_type == "summary":
            report = "=== DATA SUMMARY ===\n\n"
            for key, value in data_dict.items():
                if isinstance(value, dict):
                    report += f"{key.upper()}:\n"
                    for sub_key, sub_value in value.items():
                        report += f"  - {sub_key}: {sub_value}\n"
                else:
                    report += f"{key}: {value}\n"
                    
        elif format_type == "detailed":
            report = "=== DETAILED REPORT ===\n\n"
            report += json.dumps(data_dict, indent=2)
            
        else:  # table format
            report = "=== DATA TABLE ===\n\n"
            report += "Key                 | Value\n"
            report += "--------------------|------------------\n"
            for key, value in data_dict.items():
                if not isinstance(value, (dict, list)):
                    report += f"{key:20}| {value}\n"
        
        return report
        
    except Exception as e:
        return f"Error formatting report: {str(e)}"
