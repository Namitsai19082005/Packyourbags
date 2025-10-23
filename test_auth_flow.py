#!/usr/bin/env python3
"""
Authentication Flow Test
Tests the complete login -> profile check flow
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_complete_auth_flow():
    """Test the complete authentication flow"""
    print("=" * 60)
    print("AUTHENTICATION FLOW TEST")
    print("=" * 60)
    
    # Step 1: Test Login
    print("Step 1: Testing Login...")
    login_data = {
        "username": "testuser456",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            user = data.get('user')
            print(f"✅ Login successful!")
            print(f"   Token: {token[:50]}...")
            print(f"   User: {user.get('username')} ({user.get('role')})")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 2: Test Profile API with Token
    print("\nStep 2: Testing Profile API...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        if response.status_code == 200:
            profile_data = response.json()
            print(f"✅ Profile API successful!")
            print(f"   User ID: {profile_data['user']['id']}")
            print(f"   Username: {profile_data['user']['username']}")
            print(f"   Email: {profile_data['user']['email']}")
        else:
            print(f"❌ Profile API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Profile API error: {e}")
        return False
    
    # Step 3: Test Packages API (should work without auth)
    print("\nStep 3: Testing Packages API...")
    try:
        response = requests.get(f"{BASE_URL}/packages/")
        if response.status_code == 200:
            packages_data = response.json()
            print(f"✅ Packages API successful!")
            print(f"   Found {packages_data.get('total', 0)} packages")
        else:
            print(f"❌ Packages API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Packages API error: {e}")
        return False
    
    # Step 4: Test Bookings API (requires auth)
    print("\nStep 4: Testing Bookings API...")
    try:
        response = requests.get(f"{BASE_URL}/bookings", headers=headers)
        if response.status_code == 200:
            print(f"✅ Bookings API successful!")
        else:
            print(f"❌ Bookings API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Bookings API error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("ALL AUTHENTICATION TESTS PASSED!")
    print("Login -> Token -> Profile -> Protected APIs working!")
    print("=" * 60)
    
    return True

def test_cors_headers():
    """Test CORS headers"""
    print("\nTesting CORS Headers...")
    try:
        response = requests.options(f"{BASE_URL}/auth/login")
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
        }
        print(f"CORS Headers: {cors_headers}")
        return True
    except Exception as e:
        print(f"CORS test error: {e}")
        return False

if __name__ == "__main__":
    print("TOURISM MANAGEMENT SYSTEM - AUTHENTICATION FLOW TEST")
    
    # Test CORS
    test_cors_headers()
    
    # Test complete auth flow
    if test_complete_auth_flow():
        print("\nAUTHENTICATION SYSTEM IS FULLY WORKING!")
        print("Your React frontend should now stay logged in properly!")
        print("Access your app at: http://localhost:5000")
    else:
        print("\nAuthentication system has issues that need to be fixed.")
