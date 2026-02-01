#!/usr/bin/env python3
"""
Test script for multi-auth FastAPI backend
Tests all authentication methods: Basic, Bearer, API Key, and Key-Value
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"

# Test credentials for each auth type
AUTH_METHODS = {
    "basic": {
        "name": "Basic Auth",
        "credentials": ("demo", "demo123"),
        "headers": {}
    },
    "bearer": {
        "name": "Bearer Token",
        "credentials": None,
        "headers": {"Authorization": "Bearer demo-token-456"}
    },
    "api_key": {
        "name": "API Key",
        "credentials": None,
        "headers": {"x-api-key": "demo-api-key"}
    },
    "key_value": {
        "name": "Key-Value Headers",
        "credentials": None,
        "headers": {"x-client-id": "client-123"}
    }
}

# Color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def print_header(text):
    """Print a header"""
    print(f"\n{BLUE}{'='*70}{NC}")
    print(f"{BLUE}{text:^70}{NC}")
    print(f"{BLUE}{'='*70}{NC}\n")

def print_test(name, passed, details=""):
    """Print test result"""
    status = f"{GREEN}✓ PASS{NC}" if passed else f"{RED}✗ FAIL{NC}"
    print(f"{status} - {name}")
    if details:
        print(f"  {details}")

def test_auth_method(method_name, endpoint="/api/v1/data"):
    """Test a specific authentication method"""
    auth_config = AUTH_METHODS[method_name]
    
    try:
        kwargs = {"timeout": 5}
        if auth_config["credentials"]:
            kwargs["auth"] = HTTPBasicAuth(*auth_config["credentials"])
        if auth_config["headers"]:
            kwargs["headers"] = auth_config["headers"]
        
        response = requests.get(f"{BASE_URL}{endpoint}", **kwargs)
        
        if response.status_code == 200:
            data = response.json()
            auth_method_used = data.get("auth_method", "unknown")
            print_test(
                f"{auth_config['name']} on {endpoint}",
                True,
                f"Status: {response.status_code}, Auth method: {auth_method_used}"
            )
            return True
        else:
            print_test(
                f"{auth_config['name']} on {endpoint}",
                False,
                f"Status: {response.status_code}"
            )
            return False
    except Exception as e:
        print_test(
            f"{auth_config['name']} on {endpoint}",
            False,
            f"Error: {str(e)}"
        )
        return False

def test_specific_auth_endpoint(method_name):
    """Test the specific auth-only endpoints"""
    endpoint_map = {
        "basic": "/api/v1/auth/basic-only",
        "bearer": "/api/v1/auth/bearer-only",
        "api_key": "/api/v1/auth/apikey-only",
        "key_value": "/api/v1/auth/keyvalue-only"
    }
    
    endpoint = endpoint_map.get(method_name)
    if not endpoint:
        return False
    
    return test_auth_method(method_name, endpoint)

def test_wrong_auth_rejected():
    """Test that wrong authentication is rejected"""
    print_header("Testing Authentication Rejection")
    
    tests_passed = 0
    total_tests = 0
    
    # Test with no auth
    total_tests += 1
    try:
        response = requests.get(f"{BASE_URL}/api/v1/data", timeout=5)
        if response.status_code == 401:
            print_test("No authentication rejected", True, "Status: 401")
            tests_passed += 1
        else:
            print_test("No authentication rejected", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("No authentication rejected", False, str(e))
    
    # Test with wrong basic auth
    total_tests += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/data",
            auth=HTTPBasicAuth("wrong", "wrong"),
            timeout=5
        )
        if response.status_code == 401:
            print_test("Wrong basic auth rejected", True, "Status: 401")
            tests_passed += 1
        else:
            print_test("Wrong basic auth rejected", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Wrong basic auth rejected", False, str(e))
    
    # Test with wrong bearer token
    total_tests += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/data",
            headers={"Authorization": "Bearer invalid-token"},
            timeout=5
        )
        if response.status_code == 401:
            print_test("Wrong bearer token rejected", True, "Status: 401")
            tests_passed += 1
        else:
            print_test("Wrong bearer token rejected", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Wrong bearer token rejected", False, str(e))
    
    # Test with wrong API key
    total_tests += 1
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/data",
            headers={"x-api-key": "invalid-key"},
            timeout=5
        )
        if response.status_code == 401:
            print_test("Wrong API key rejected", True, "Status: 401")
            tests_passed += 1
        else:
            print_test("Wrong API key rejected", False, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Wrong API key rejected", False, str(e))
    
    return tests_passed, total_tests

def main():
    """Run all authentication tests"""
    print_header("FastAPI Multi-Auth Backend Test Suite")
    
    print(f"{YELLOW}Testing server at: {BASE_URL}{NC}\n")
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=2)
        info = response.json()
        print(f"{GREEN}✓ Server is running{NC}")
        print(f"{YELLOW}Supported auth methods: {', '.join(info.get('authentication', {}).get('supported_methods', []))}{NC}\n")
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗ ERROR: Cannot connect to server at {BASE_URL}{NC}")
        print(f"{YELLOW}Make sure the server is running:{NC}")
        print(f"  cd backend && ./run_server.sh start-dev")
        sys.exit(1)
    
    total_tests = 0
    passed_tests = 0
    
    # Test flexible authentication on general endpoints
    print_header("Testing Flexible Authentication (Any Method Accepted)")
    
    endpoints = ["/api/v1/data", "/api/v1/users/123", "/api/v1/products", "/api/v1/dashboard"]
    
    for method_name in AUTH_METHODS.keys():
        for endpoint in endpoints:
            total_tests += 1
            if test_auth_method(method_name, endpoint):
                passed_tests += 1
    
    # Test specific authentication endpoints
    print_header("Testing Specific Authentication Endpoints")
    
    for method_name in AUTH_METHODS.keys():
        total_tests += 1
        if test_specific_auth_endpoint(method_name):
            passed_tests += 1
    
    # Test rejection of wrong auth
    rejected_passed, rejected_total = test_wrong_auth_rejected()
    passed_tests += rejected_passed
    total_tests += rejected_total
    
    # Summary
    print_header("Test Summary")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    if passed_tests == total_tests:
        print(f"{GREEN}✓ All tests passed! ({passed_tests}/{total_tests}){NC}")
    else:
        print(f"{YELLOW}Tests passed: {passed_tests}/{total_tests} ({success_rate:.1f}%){NC}")
        print(f"{RED}Tests failed: {total_tests - passed_tests}{NC}")
    
    print(f"\n{BLUE}Authentication Methods Tested:{NC}")
    for method_name, config in AUTH_METHODS.items():
        print(f"  • {config['name']}")
    
    print()
    
    # Exit code
    sys.exit(0 if passed_tests == total_tests else 1)

if __name__ == "__main__":
    main()