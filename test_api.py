#!/usr/bin/env python3
"""
API Test Script for Tourism Management System
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure the app is running.")
        return False

def test_user_registration():
    """Test user registration"""
    print("Testing user registration...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "phone_number": "+1234567890",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        if response.status_code == 201:
            print("✓ User registration successful")
            return response.json().get('access_token')
        else:
            print(f"✗ User registration failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Registration error: {e}")
        return None

def test_user_login():
    """Test user login"""
    print("Testing user login...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            print("✓ User login successful")
            return response.json().get('access_token')
        else:
            print(f"✗ User login failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None

def test_get_packages(token=None):
    """Test getting packages"""
    print("Testing get packages...")
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        response = requests.get(f"{BASE_URL}/api/packages", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Packages retrieved successfully ({len(data.get('packages', []))} packages)")
            return True
        else:
            print(f"✗ Get packages failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Get packages error: {e}")
        return False

def test_get_destinations():
    """Test getting destinations"""
    print("Testing get destinations...")
    try:
        response = requests.get(f"{BASE_URL}/api/packages/destinations")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Destinations retrieved successfully ({len(data.get('destinations', []))} destinations)")
            return True
        else:
            print(f"✗ Get destinations failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Get destinations error: {e}")
        return False

def test_create_booking(token):
    """Test creating a booking"""
    print("Testing create booking...")
    if not token:
        print("✗ No token available for booking test")
        return False
    
    # First get a package ID
    try:
        response = requests.get(f"{BASE_URL}/api/packages")
        if response.status_code == 200:
            packages = response.json().get('packages', [])
            if packages:
                package_id = packages[0]['id']
                
                booking_data = {
                    "package_id": package_id,
                    "booking_date": "2024-12-25",
                    "number_of_travelers": 2
                }
                
                headers = {'Authorization': f'Bearer {token}'}
                response = requests.post(f"{BASE_URL}/api/bookings", json=booking_data, headers=headers)
                
                if response.status_code == 201:
                    print("✓ Booking created successfully")
                    return True
                else:
                    print(f"✗ Create booking failed: {response.status_code}")
                    print(f"Response: {response.text}")
                    return False
            else:
                print("✗ No packages available for booking test")
                return False
        else:
            print("✗ Could not get packages for booking test")
            return False
    except Exception as e:
        print(f"✗ Create booking error: {e}")
        return False

def test_admin_stats(token):
    """Test admin statistics"""
    print("Testing admin statistics...")
    if not token:
        print("✗ No token available for admin test")
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get(f"{BASE_URL}/api/admin/stats", headers=headers)
        if response.status_code == 200:
            print("✓ Admin stats retrieved successfully")
            return True
        else:
            print(f"✗ Admin stats failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Admin stats error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("Tourism Management System API Tests")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("\n❌ Health check failed. Please start the application first.")
        sys.exit(1)
    
    print("\n" + "-" * 30)
    
    # Test user registration
    token = test_user_registration()
    
    # Test user login (admin)
    admin_token = test_user_login()
    
    print("\n" + "-" * 30)
    
    # Test public endpoints
    test_get_packages()
    test_get_destinations()
    
    print("\n" + "-" * 30)
    
    # Test authenticated endpoints
    if token:
        test_get_packages(token)
        test_create_booking(token)
    
    if admin_token:
        test_admin_stats(admin_token)
    
    print("\n" + "=" * 50)
    print("API tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
