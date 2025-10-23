#!/usr/bin/env python3
"""
Final Authentication Test
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_auth():
    print("=" * 60)
    print("AUTHENTICATION TEST")
    print("=" * 60)
    
    # Test Login
    print("Testing Login...")
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
            print(f"SUCCESS: Login successful!")
            print(f"Token: {token[:50]}...")
            print(f"User: {user.get('username')} ({user.get('role')})")
        else:
            print(f"FAILED: Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Login error: {e}")
        return False
    
    # Test Profile API
    print("\nTesting Profile API...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        if response.status_code == 200:
            profile_data = response.json()
            print(f"SUCCESS: Profile API successful!")
            print(f"User ID: {profile_data['user']['id']}")
            print(f"Username: {profile_data['user']['username']}")
        else:
            print(f"FAILED: Profile API failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Profile API error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("Authentication system is working correctly!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    if test_auth():
        print("\nAUTHENTICATION SYSTEM IS FULLY WORKING!")
        print("Your React frontend should now stay logged in properly!")
        print("Access your app at: http://localhost:5000")
    else:
        print("\nAuthentication system has issues.")
