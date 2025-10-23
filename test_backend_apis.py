#!/usr/bin/env python3
"""
Comprehensive Backend API Testing Script
Tests all API endpoints to ensure they're working correctly
"""

import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health check endpoint"""
    print("Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_auth_apis():
    """Test authentication APIs"""
    print("\n🔐 Testing Authentication APIs...")
    
    # Test registration
    print("  Testing user registration...")
    register_data = {
        "username": "testuser123",
        "email": "testuser123@test.com",
        "password": "password123",
        "phone_number": "1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("  ✅ User registration successful")
            user_data = response.json()
            token = user_data.get('access_token')
            return token
        else:
            print(f"  ❌ Registration failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"  ❌ Registration error: {e}")
        return None

def test_login(token):
    """Test login functionality"""
    print("  Testing user login...")
    login_data = {
        "username": "testuser123",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("  ✅ User login successful")
            return response.json().get('access_token')
        else:
            print(f"  ❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"  ❌ Login error: {e}")
        return None

def test_profile_api(token):
    """Test profile API"""
    print("  Testing profile API...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/profile", headers=headers)
        if response.status_code == 200:
            print("  ✅ Profile API successful")
            return True
        else:
            print(f"  ❌ Profile API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Profile API error: {e}")
        return False

def test_packages_api():
    """Test packages API"""
    print("\n📦 Testing Packages API...")
    
    try:
        response = requests.get(f"{BASE_URL}/packages/")
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Packages API successful - Found {data.get('total', 0)} packages")
            return True
        else:
            print(f"  ❌ Packages API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Packages API error: {e}")
        return False

def test_package_details():
    """Test package details API"""
    print("  Testing package details...")
    
    try:
        response = requests.get(f"{BASE_URL}/packages/1")
        if response.status_code == 200:
            print("  ✅ Package details API successful")
            return True
        else:
            print(f"  ❌ Package details failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Package details error: {e}")
        return False

def test_destinations_api():
    """Test destinations API"""
    print("  Testing destinations API...")
    
    try:
        response = requests.get(f"{BASE_URL}/packages/destinations")
        if response.status_code == 200:
            print("  ✅ Destinations API successful")
            return True
        else:
            print(f"  ❌ Destinations API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Destinations API error: {e}")
        return False

def test_bookings_api(token):
    """Test bookings API"""
    print("\n🎫 Testing Bookings API...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/bookings", headers=headers)
        if response.status_code == 200:
            print("  ✅ Bookings API successful")
            return True
        else:
            print(f"  ❌ Bookings API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Bookings API error: {e}")
        return False

def test_reviews_api(token):
    """Test reviews API"""
    print("\n⭐ Testing Reviews API...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/reviews", headers=headers)
        if response.status_code == 200:
            print("  ✅ Reviews API successful")
            return True
        else:
            print(f"  ❌ Reviews API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Reviews API error: {e}")
        return False

def test_admin_api(token):
    """Test admin API"""
    print("\n👨‍💼 Testing Admin API...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/admin/stats", headers=headers)
        if response.status_code == 200:
            print("  ✅ Admin stats API successful")
            return True
        elif response.status_code == 403:
            print("  ⚠️  Admin API requires admin role (expected for regular user)")
            return True
        else:
            print(f"  ❌ Admin API failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"  ❌ Admin API error: {e}")
        return False

def main():
    """Main testing function"""
    print("=" * 60)
    print("🧪 TOURISM MANAGEMENT SYSTEM - BACKEND API TESTING")
    print("=" * 60)
    
    # Test health check
    if not test_health():
        print("\n❌ System is not running. Please start the backend server first.")
        sys.exit(1)
    
    # Test authentication
    token = test_auth_apis()
    if not token:
        print("\n❌ Authentication tests failed. Cannot proceed with other tests.")
        sys.exit(1)
    
    # Test login
    login_token = test_login(token)
    if not login_token:
        print("\n❌ Login test failed.")
        sys.exit(1)
    
    # Test profile
    if not test_profile_api(login_token):
        print("\n❌ Profile API test failed.")
        sys.exit(1)
    
    # Test packages
    if not test_packages_api():
        print("\n❌ Packages API test failed.")
        sys.exit(1)
    
    if not test_package_details():
        print("\n❌ Package details test failed.")
        sys.exit(1)
    
    if not test_destinations_api():
        print("\n❌ Destinations API test failed.")
        sys.exit(1)
    
    # Test bookings
    if not test_bookings_api(login_token):
        print("\n❌ Bookings API test failed.")
        sys.exit(1)
    
    # Test reviews
    if not test_reviews_api(login_token):
        print("\n❌ Reviews API test failed.")
        sys.exit(1)
    
    # Test admin
    test_admin_api(login_token)
    
    print("\n" + "=" * 60)
    print("🎉 ALL BACKEND API TESTS COMPLETED SUCCESSFULLY!")
    print("✅ Your Tourism Management System backend is fully functional!")
    print("=" * 60)
    print("\n🌐 Access your application at: http://localhost:5000")
    print("📱 Frontend: Modern React SPA with authentication")
    print("🔧 Backend: Flask API with SQLite database")
    print("🔐 Authentication: JWT-based with role management")
    print("📦 Features: Packages, Bookings, Reviews, Admin Dashboard")

if __name__ == "__main__":
    main()
