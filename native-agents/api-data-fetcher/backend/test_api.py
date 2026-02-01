#!/usr/bin/env python3
"""
Test script for the FastAPI backend API
Tests all endpoints and authentication
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import sys

# Configuration
BASE_URL = "http://localhost:8000"
VALID_USER = "demo"
VALID_PASS = "demo123"

# Color codes for output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

def print_test(name, passed, details=""):
    """Print test result"""
    status = f"{GREEN}✓ PASS{NC}" if passed else f"{RED}✗ FAIL{NC}"
    print(f"{status} - {name}")
    if details:
        print(f"  {details}")

def test_health_endpoint():
    """Test health endpoint (no auth required)"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        passed = response.status_code == 200
        print_test("Health endpoint", passed, 
                  f"Status: {response.status_code}, Response: {response.json()}")
        return passed
    except Exception as e:
        print_test("Health endpoint", False, f"Error: {str(e)}")
        return False

def test_root_endpoint():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        passed = response.status_code == 200 and "version" in response.json()
        print_test("Root endpoint", passed, 
                  f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Root endpoint", False, f"Error: {str(e)}")
        return False

def test_auth_success():
    """Test successful authentication"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/data",
            auth=HTTPBasicAuth(VALID_USER, VALID_PASS),
            timeout=5
        )
        passed = response.status_code == 200 and response.json().get("success") == True
        print_test("Authentication (valid credentials)", passed,
                  f"Status: {response.status_code}, Authenticated as: {response.json().get('authenticated_as')}")
        return passed
    except Exception as e:
        print_test("Authentication (valid credentials)", False, f"Error: {str(e)}")
        return False

def test_auth_failure():
    """Test failed authentication"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/data",
            auth=HTTPBasicAuth("wrong", "wrong"),
            timeout=5
        )
        passed = response.status_code == 401
        print_test("Authentication (invalid credentials)", passed,
                  f"Status: {response.status_code} (expected 401)")
        return passed
    except Exception as e:
        print_test("Authentication (invalid credentials)", False, f"Error: {str(e)}")
        return False

def test_get_user():
    """Test get user endpoint"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/users/123",
            auth=HTTPBasicAuth(VALID_USER, VALID_PASS),
            timeout=5
        )
        data = response.json()
        passed = (response.status_code == 200 and 
                 data.get("success") == True and 
                 data.get("user", {}).get("id") == "123")
        print_test("Get user by ID", passed,
                  f"Status: {response.status_code}, User: {data.get('user', {}).get('username')}")
        return passed
    except Exception as e:
        print_test("Get user by ID", False, f"Error: {str(e)}")
        return False

def test_list_products():
    """Test list products endpoint"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/products",
            auth=HTTPBasicAuth(VALID_USER, VALID_PASS),
            timeout=5
        )
        data = response.json()
        passed = (response.status_code == 200 and 
                 data.get("success") == True and 
                 "data" in data)
        total = data.get("data", {}).get("total", 0)
        print_test("List products", passed,
                  f"Status: {response.status_code}, Total products: {total}")
        return passed
    except Exception as e:
        print_test("List products", False, f"Error: {str(e)}")
        return False

def test_search():
    """Test search endpoint"""
    try:
        params = {
            "q": "laptop",
            "filters": json.dumps({"status": "active"})
        }
        response = requests.get(
            f"{BASE_URL}/api/v1/search",
            params=params,
            auth=HTTPBasicAuth(VALID_USER, VALID_PASS),
            timeout=5
        )
        data = response.json()
        passed = (response.status_code == 200 and 
                 data.get("success") == True and 
                 "results" in data)
        total = data.get("total_results", 0)
        print_test("Search with filters", passed,
                  f"Status: {response.status_code}, Results found: {total}")
        return passed
    except Exception as e:
        print_test("Search with filters", False, f"Error: {str(e)}")
        return False

def test_dashboard():
    """Test dashboard endpoint"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/dashboard",
            auth=HTTPBasicAuth(VALID_USER, VALID_PASS),
            timeout=5
        )
        data = response.json()
        passed = (response.status_code == 200 and 
                 data.get("success") == True and 
                 "metrics" in data)
        metrics = data.get("metrics", {})
        print_test("Dashboard metrics", passed,
                  f"Status: {response.status_code}, Users: {metrics.get('total_users')}, Products: {metrics.get('total_products')}")
        return passed
    except Exception as e:
        print_test("Dashboard metrics", False, f"Error: {str(e)}")
        return False

def test_user_not_found():
    """Test user not found"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/users/999",
            auth=HTTPBasicAuth(VALID_USER, VALID_PASS),
            timeout=5
        )
        passed = response.status_code == 404
        print_test("User not found (404)", passed,
                  f"Status: {response.status_code} (expected 404)")
        return passed
    except Exception as e:
        print_test("User not found (404)", False, f"Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n{BLUE}{'='*60}{NC}")
    print(f"{BLUE}FastAPI Backend Test Suite{NC}")
    print(f"{BLUE}{'='*60}{NC}\n")
    
    print(f"{YELLOW}Testing server at: {BASE_URL}{NC}")
    print(f"{YELLOW}Using credentials: {VALID_USER} / {VALID_PASS}{NC}\n")
    
    # Check if server is running
    try:
        requests.get(BASE_URL, timeout=2)
    except requests.exceptions.ConnectionError:
        print(f"{RED}✗ ERROR: Cannot connect to server at {BASE_URL}{NC}")
        print(f"{YELLOW}Make sure the server is running:{NC}")
        print(f"  ./run_server.sh start-dev")
        sys.exit(1)
    
    print(f"{BLUE}Running tests...{NC}\n")
    
    # Run all tests
    tests = [
        ("Public Endpoints", [
            test_health_endpoint,
            test_root_endpoint,
        ]),
        ("Authentication", [
            test_auth_success,
            test_auth_failure,
        ]),
        ("Data Endpoints", [
            test_get_user,
            test_list_products,
            test_dashboard,
        ]),
        ("Search & Filtering", [
            test_search,
        ]),
        ("Error Handling", [
            test_user_not_found,
        ])
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for category, test_functions in tests:
        print(f"\n{BLUE}{'─'*60}{NC}")
        print(f"{BLUE}{category}{NC}")
        print(f"{BLUE}{'─'*60}{NC}\n")
        
        for test_func in test_functions:
            total_tests += 1
            if test_func():
                passed_tests += 1
    
    # Summary
    print(f"\n{BLUE}{'='*60}{NC}")
    print(f"{BLUE}Test Summary{NC}")
    print(f"{BLUE}{'='*60}{NC}\n")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    if passed_tests == total_tests:
        print(f"{GREEN}✓ All tests passed! ({passed_tests}/{total_tests}){NC}")
    else:
        print(f"{YELLOW}Tests passed: {passed_tests}/{total_tests} ({success_rate:.1f}%){NC}")
        print(f"{RED}Tests failed: {total_tests - passed_tests}{NC}")
    
    print()
    
    # Exit code
    sys.exit(0 if passed_tests == total_tests else 1)

if __name__ == "__main__":
    main()
