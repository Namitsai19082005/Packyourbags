#!/usr/bin/env python3
"""
Frontend Navigation and Data Loading Test
Tests the complete user flow from login to dashboard navigation
"""

import requests
import json
import time

def test_frontend_navigation():
    """Test complete frontend navigation and data loading"""
    
    print("=" * 60)
    print("FRONTEND NAVIGATION AND DATA LOADING TEST")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    api_url = f"{base_url}/api"
    
    # Test 1: Check if React app is being served
    print("\n1. Testing React App Serving...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200 and "react" in response.text.lower():
            print("SUCCESS: React app is being served correctly")
        else:
            print("FAILED: React app not being served properly")
            return False
    except Exception as e:
        print(f"FAILED: Error accessing React app: {e}")
        return False
    
    # Test 2: Check API endpoints are accessible
    print("\n2. Testing API Endpoints...")
    endpoints = [
        "/api/health",
        "/api/packages/",
        "/api/auth/register",
        "/api/auth/login"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            if response.status_code in [200, 405]:  # 405 is OK for POST-only endpoints
                print(f"SUCCESS: {endpoint} is accessible")
            else:
                print(f"WARNING: {endpoint} returned {response.status_code}")
        except Exception as e:
            print(f"FAILED: {endpoint} error: {e}")
    
    # Test 3: Test authentication flow
    print("\n3. Testing Authentication Flow...")
    try:
        # Register a test user
        register_data = {
            "username": "testuser_frontend",
            "email": "testuser_frontend@example.com",
            "password": "testpass123",
            "full_name": "Test User Frontend"
        }
        
        response = requests.post(f"{api_url}/auth/register", json=register_data)
        if response.status_code == 201:
            print("SUCCESS: User registration successful")
        else:
            print(f"WARNING: Registration returned {response.status_code}")
        
        # Login
        login_data = {
            "email": "testuser_frontend@example.com",
            "password": "testpass123"
        }
        
        response = requests.post(f"{api_url}/auth/login", json=login_data)
        if response.status_code == 200:
            print("SUCCESS: User login successful")
            token = response.json().get('access_token')
            if token:
                print("SUCCESS: JWT token received")
                
                # Test protected endpoint
                headers = {"Authorization": f"Bearer {token}"}
                profile_response = requests.get(f"{api_url}/auth/profile", headers=headers)
                if profile_response.status_code == 200:
                    print("SUCCESS: Protected endpoint accessible with token")
                    user_data = profile_response.json()
                    print(f"User role: {user_data.get('user', {}).get('role', 'unknown')}")
                else:
                    print(f"FAILED: Protected endpoint returned {profile_response.status_code}")
            else:
                print("FAILED: No JWT token in response")
        else:
            print(f"FAILED: Login returned {response.status_code}")
            
    except Exception as e:
        print(f"FAILED: Authentication flow error: {e}")
    
    # Test 4: Test packages data
    print("\n4. Testing Packages Data...")
    try:
        response = requests.get(f"{api_url}/packages/")
        if response.status_code == 200:
            data = response.json()
            packages = data.get('packages', [])
            print(f"SUCCESS: Found {len(packages)} packages")
            
            if packages:
                print("Sample package data:")
                sample = packages[0]
                print(f"  - Title: {sample.get('title', 'N/A')}")
                print(f"  - Destination: {sample.get('destination', 'N/A')}")
                print(f"  - Price: ${sample.get('price', 'N/A')}")
                print(f"  - Duration: {sample.get('duration', 'N/A')} days")
        else:
            print(f"FAILED: Packages API returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Packages data error: {e}")
    
    # Test 5: Test CORS configuration
    print("\n5. Testing CORS Configuration...")
    try:
        response = requests.options(f"{api_url}/packages/")
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials')
        }
        print(f"CORS Headers: {cors_headers}")
        
        if cors_headers['Access-Control-Allow-Origin']:
            print("SUCCESS: CORS is properly configured")
        else:
            print("WARNING: CORS might not be properly configured")
    except Exception as e:
        print(f"FAILED: CORS test error: {e}")
    
    print("\n" + "=" * 60)
    print("FRONTEND NAVIGATION TEST COMPLETED!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Open your browser and go to: http://localhost:5000")
    print("2. Register a new account or login with existing credentials")
    print("3. Check if the dashboard shows packages and stats")
    print("4. Test navigation between different pages")
    print("5. Verify that all buttons and links are working")
    
    return True

if __name__ == "__main__":
    test_frontend_navigation()
