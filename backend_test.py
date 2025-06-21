#!/usr/bin/env python3
import requests
import json
import time
import sys
from typing import Dict, Any, Optional, Tuple

# Get the backend URL from the frontend .env file
BACKEND_URL = "https://0d67eaf5-ec7d-486f-8e33-966d75d70c03.preview.emergentagent.com"
API_URL = f"{BACKEND_URL}/api"

# Test data
ADMIN_EMAIL = "zagat5654@gmail.com"
ADMIN_PASSWORD = "admin123"

# Sample repair request data
REPAIR_REQUEST_DATA = {
    "customerName": "John Doe",
    "customerEmail": "john@example.com",
    "customerPhone": "+1234567890",
    "deviceBrand": "iPhone",
    "deviceModel": "iPhone 15 Pro",
    "issueCategory": "Screen Issues",
    "specificIssue": "Cracked Screen",
    "description": "Screen cracked after dropping the phone",
    "urgency": "normal",
    "pickupAddress": "123 Main St, City, State",
    "pickupTime": "9am-12pm",
    "gdprConsent": True
}

# Sample contact message data
CONTACT_MESSAGE_DATA = {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "subject": "Question about pricing",
    "message": "I would like to know more about your repair pricing."
}

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.total = 0
        self.auth_token = None
        self.created_ticket_id = None
    
    def add_result(self, test_name: str, passed: bool, response: Optional[requests.Response] = None, error: Optional[str] = None):
        self.total += 1
        if passed:
            self.passed += 1
            status = "✅ PASSED"
        else:
            self.failed += 1
            status = "❌ FAILED"
        
        print(f"{status} - {test_name}")
        
        if response:
            try:
                print(f"  Status Code: {response.status_code}")
                print(f"  Response: {json.dumps(response.json(), indent=2)}")
            except:
                print(f"  Response: {response.text[:200]}")
        
        if error:
            print(f"  Error: {error}")
        
        print("-" * 80)
    
    def print_summary(self):
        print("\n" + "=" * 80)
        print(f"TEST SUMMARY: {self.passed}/{self.total} tests passed ({self.passed/self.total*100:.1f}%)")
        print(f"  ✅ Passed: {self.passed}")
        print(f"  ❌ Failed: {self.failed}")
        print("=" * 80)
        
        if self.failed > 0:
            return 1
        return 0


def make_request(method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                 headers: Optional[Dict[str, str]] = None, 
                 expected_status: int = 200) -> Tuple[bool, requests.Response, Optional[str]]:
    """Make an HTTP request and return success status, response and error message."""
    url = f"{API_URL}{endpoint}"
    
    try:
        if method.lower() == "get":
            response = requests.get(url, headers=headers)
        elif method.lower() == "post":
            response = requests.post(url, json=data, headers=headers)
        elif method.lower() == "put":
            response = requests.put(url, json=data, headers=headers)
        elif method.lower() == "delete":
            response = requests.delete(url, headers=headers)
        else:
            return False, None, f"Unsupported method: {method}"
        
        success = response.status_code == expected_status
        error = None if success else f"Expected status {expected_status}, got {response.status_code}"
        return success, response, error
    
    except Exception as e:
        return False, None, str(e)


def test_health_check(results: TestResult):
    """Test the health check endpoint."""
    success, response, error = make_request("get", "/health")
    results.add_result("Health Check", success, response, error)


def test_login_success(results: TestResult):
    """Test successful login."""
    data = {"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    success, response, error = make_request("post", "/auth/login", data)
    
    if success and 'access_token' in response.json():
        results.auth_token = response.json()['access_token']
    
    results.add_result("Login Success", success, response, error)


def test_login_failure(results: TestResult):
    """Test login with incorrect credentials."""
    data = {"email": ADMIN_EMAIL, "password": "wrong_password"}
    success, response, error = make_request("post", "/auth/login", data, expected_status=401)
    results.add_result("Login Failure (Wrong Password)", success, response, error)


def test_get_current_user(results: TestResult):
    """Test getting current user information."""
    if not results.auth_token:
        results.add_result("Get Current User", False, None, "No auth token available")
        return
    
    headers = {"Authorization": f"Bearer {results.auth_token}"}
    success, response, error = make_request("get", "/auth/me", headers=headers)
    results.add_result("Get Current User", success, response, error)


def test_validate_token(results: TestResult):
    """Test token validation."""
    if not results.auth_token:
        results.add_result("Validate Token", False, None, "No auth token available")
        return
    
    headers = {"Authorization": f"Bearer {results.auth_token}"}
    success, response, error = make_request("get", "/auth/validate-token", headers=headers)
    results.add_result("Validate Token", success, response, error)


def test_unauthorized_access(results: TestResult):
    """Test accessing protected endpoint without authentication."""
    success, response, error = make_request("get", "/repair-requests/", expected_status=401)
    results.add_result("Unauthorized Access", success, response, error)


def test_create_repair_request(results: TestResult):
    """Test creating a new repair request."""
    success, response, error = make_request("post", "/repair-requests/", REPAIR_REQUEST_DATA)
    
    if success and response.json().get('success') and 'ticket_id' in response.json():
        results.created_ticket_id = response.json()['ticket_id']
    
    results.add_result("Create Repair Request", success, response, error)


def test_get_repair_requests(results: TestResult):
    """Test getting all repair requests."""
    if not results.auth_token:
        results.add_result("Get Repair Requests", False, None, "No auth token available")
        return
    
    headers = {"Authorization": f"Bearer {results.auth_token}"}
    success, response, error = make_request("get", "/repair-requests/", headers=headers)
    results.add_result("Get Repair Requests", success, response, error)


def test_update_repair_status(results: TestResult):
    """Test updating repair request status."""
    if not results.auth_token or not results.created_ticket_id:
        results.add_result("Update Repair Status", False, None, 
                          "No auth token or ticket ID available")
        return
    
    headers = {"Authorization": f"Bearer {results.auth_token}"}
    data = {
        "ticket_id": results.created_ticket_id,
        "status": "In Progress",
        "notes": "Started working on the repair"
    }
    
    success, response, error = make_request(
        "put", f"/repair-requests/{results.created_ticket_id}/status", 
        data, headers
    )
    
    results.add_result("Update Repair Status", success, response, error)


def test_create_contact_message(results: TestResult):
    """Test creating a contact message."""
    success, response, error = make_request("post", "/contact/", CONTACT_MESSAGE_DATA)
    results.add_result("Create Contact Message", success, response, error)


def test_invalid_data(results: TestResult):
    """Test submitting invalid data."""
    # Missing required fields
    invalid_data = {
        "customerName": "John Doe",
        # Missing email and other required fields
        "deviceBrand": "iPhone"
    }
    
    success, response, error = make_request("post", "/repair-requests/", invalid_data, expected_status=422)
    results.add_result("Invalid Data Handling", success, response, error)


def main():
    print("\n" + "=" * 80)
    print("FIXNET BACKEND API TESTING")
    print("=" * 80)
    
    results = TestResult()
    
    # Basic health check
    test_health_check(results)
    
    # Authentication tests
    test_login_success(results)
    test_login_failure(results)
    test_get_current_user(results)
    test_validate_token(results)
    test_unauthorized_access(results)
    
    # Repair request tests
    test_create_repair_request(results)
    test_get_repair_requests(results)
    test_update_repair_status(results)
    
    # Contact message test
    test_create_contact_message(results)
    
    # Error handling test
    test_invalid_data(results)
    
    # Print summary
    return results.print_summary()


if __name__ == "__main__":
    sys.exit(main())