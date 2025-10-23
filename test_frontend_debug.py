#!/usr/bin/env python3
"""
Frontend Debug Test - Check if React app is loading and making API calls
"""

import requests
import json

def test_frontend_debug():
    """Test frontend loading and API integration"""
    
    print("=" * 60)
    print("FRONTEND DEBUG TEST")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Check if React app loads
    print("\n1. Testing React App Loading...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            content = response.text
            if "root" in content and "main." in content:
                print("SUCCESS: React app HTML is being served")
                print(f"Content length: {len(content)} characters")
            else:
                print("WARNING: React app might not be properly built")
        else:
            print(f"FAILED: HTTP {response.status_code}")
    except Exception as e:
        print(f"FAILED: {e}")
    
    # Test 2: Check if static files are accessible
    print("\n2. Testing Static Files...")
    static_files = [
        "/static/js/main.753125a6.js",
        "/static/css/main.1bd8ad7f.css"
    ]
    
    for file_path in static_files:
        try:
            response = requests.get(f"{base_url}{file_path}")
            if response.status_code == 200:
                print(f"SUCCESS: {file_path} is accessible")
            else:
                print(f"FAILED: {file_path} returned {response.status_code}")
        except Exception as e:
            print(f"FAILED: {file_path} error: {e}")
    
    # Test 3: Test API endpoints
    print("\n3. Testing API Endpoints...")
    api_endpoints = [
        "/api/health",
        "/api/packages/",
        "/api/auth/register",
        "/api/auth/login"
    ]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code in [200, 405]:
                print(f"SUCCESS: {endpoint} is accessible")
            else:
                print(f"WARNING: {endpoint} returned {response.status_code}")
        except Exception as e:
            print(f"FAILED: {endpoint} error: {e}")
    
    # Test 4: Test authentication flow
    print("\n4. Testing Authentication Flow...")
    try:
        # Register a test user
        register_data = {
            "username": "debuguser",
            "email": "debuguser@example.com",
            "password": "testpass123",
            "full_name": "Debug User"
        }
        
        response = requests.post(f"{base_url}/api/auth/register", json=register_data)
        if response.status_code == 201:
            print("SUCCESS: User registration works")
        else:
            print(f"WARNING: Registration returned {response.status_code}")
        
        # Login
        login_data = {
            "email": "debuguser@example.com",
            "password": "testpass123"
        }
        
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        if response.status_code == 200:
            print("SUCCESS: User login works")
            token = response.json().get('access_token')
            if token:
                print("SUCCESS: JWT token received")
                
                # Test protected endpoint
                headers = {"Authorization": f"Bearer {token}"}
                profile_response = requests.get(f"{base_url}/api/auth/profile", headers=headers)
                if profile_response.status_code == 200:
                    print("SUCCESS: Protected endpoints work")
                    user_data = profile_response.json()
                    print(f"User role: {user_data.get('user', {}).get('role', 'unknown')}")
                else:
                    print(f"FAILED: Protected endpoint returned {profile_response.status_code}")
        else:
            print(f"FAILED: Login returned {response.status_code}")
            
    except Exception as e:
        print(f"FAILED: Authentication error: {e}")
    
    print("\n" + "=" * 60)
    print("DEBUG TEST COMPLETED!")
    print("=" * 60)
    print("\nIf all tests pass, the issue might be:")
    print("1. JavaScript errors in the browser console")
    print("2. CORS issues preventing API calls")
    print("3. Authentication state not persisting")
    print("4. React components not re-rendering after data fetch")
    print("\nTo debug further:")
    print("1. Open browser developer tools (F12)")
    print("2. Check Console tab for JavaScript errors")
    print("3. Check Network tab for failed API calls")
    print("4. Go to http://localhost:5000 and test manually")

if __name__ == "__main__":
    test_frontend_debug()


