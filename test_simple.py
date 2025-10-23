#!/usr/bin/env python3
"""
Simple Backend API Testing Script
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health check endpoint"""
    print("Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("SUCCESS: Health check passed")
            return True
        else:
            print(f"FAILED: Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Health check error: {e}")
        return False

def test_packages():
    """Test packages API"""
    print("Testing Packages API...")
    try:
        response = requests.get(f"{BASE_URL}/packages/")
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Found {data.get('total', 0)} packages")
            return True
        else:
            print(f"FAILED: Packages API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Packages API error: {e}")
        return False

def test_auth():
    """Test authentication"""
    print("Testing Authentication...")
    
    # Test registration
    register_data = {
        "username": "testuser456",
        "email": "testuser456@test.com",
        "password": "password123",
        "phone_number": "1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("SUCCESS: User registration successful")
            token = response.json().get('access_token')
            
            # Test login
            login_data = {
                "username": "testuser456",
                "password": "password123"
            }
            
            response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                print("SUCCESS: User login successful")
                return True
            else:
                print(f"FAILED: Login failed: {response.status_code}")
                return False
        else:
            print(f"FAILED: Registration failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Auth error: {e}")
        return False

def main():
    """Main testing function"""
    print("=" * 60)
    print("TOURISM MANAGEMENT SYSTEM - BACKEND API TESTING")
    print("=" * 60)
    
    # Test health check
    if not test_health():
        print("\nERROR: System is not running. Please start the backend server first.")
        return
    
    # Test packages
    if not test_packages():
        print("\nERROR: Packages API test failed.")
        return
    
    # Test authentication
    if not test_auth():
        print("\nERROR: Authentication tests failed.")
        return
    
    print("\n" + "=" * 60)
    print("ALL BACKEND API TESTS COMPLETED SUCCESSFULLY!")
    print("Your Tourism Management System backend is fully functional!")
    print("=" * 60)
    print("\nAccess your application at: http://localhost:5000")
    print("Frontend: Modern React SPA with authentication")
    print("Backend: Flask API with SQLite database")

if __name__ == "__main__":
    main()
