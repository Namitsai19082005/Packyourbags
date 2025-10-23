#!/usr/bin/env python3
"""
Test New Features: Separate Login/Register Pages, Admin Dashboard, Profile Management
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_new_features():
    """Test all the new features"""
    print("=" * 60)
    print("TESTING NEW FEATURES")
    print("=" * 60)
    
    # Test 1: Separate Login Page
    print("\n1. Testing Separate Login Page...")
    try:
        response = requests.get(f"{BASE_URL}/login")
        if response.status_code == 200:
            print("✅ Login page loads successfully")
        else:
            print("❌ Login page failed to load")
    except Exception as e:
        print(f"❌ Login page error: {e}")
    
    # Test 2: Separate Register Page
    print("\n2. Testing Separate Register Page...")
    try:
        response = requests.get(f"{BASE_URL}/register")
        if response.status_code == 200:
            print("✅ Register page loads successfully")
        else:
            print("❌ Register page failed to load")
    except Exception as e:
        print(f"❌ Register page error: {e}")
    
    # Test 3: User Registration
    print("\n3. Testing User Registration...")
    try:
        user_data = {
            "username": "testuser_new",
            "email": "testuser_new@example.com",
            "phone_number": "+1234567890",
            "password": "testpass123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        if response.status_code == 201:
            data = response.json()
            auth_token = data.get('access_token')
            print("✅ User registration successful")
            
            # Test 4: Profile Page Access
            print("\n4. Testing Profile Page Access...")
            try:
                headers = {'Authorization': f'Bearer {auth_token}'}
                response = requests.get(f"{BASE_URL}/profile", headers=headers)
                if response.status_code == 200:
                    print("✅ Profile page accessible")
                else:
                    print("❌ Profile page not accessible")
            except Exception as e:
                print(f"❌ Profile page error: {e}")
            
            # Test 5: Bookings Page Access
            print("\n5. Testing Bookings Page Access...")
            try:
                response = requests.get(f"{BASE_URL}/bookings", headers=headers)
                if response.status_code == 200:
                    print("✅ Bookings page accessible")
                else:
                    print("❌ Bookings page not accessible")
            except Exception as e:
                print(f"❌ Bookings page error: {e}")
            
        else:
            print("❌ User registration failed")
            return
            
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Test 6: Admin Login
    print("\n6. Testing Admin Login...")
    try:
        admin_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", json=admin_data)
        if response.status_code == 200:
            data = response.json()
            admin_token = data.get('access_token')
            print("✅ Admin login successful")
            
            # Test 7: Admin Dashboard Access
            print("\n7. Testing Admin Dashboard Access...")
            try:
                headers = {'Authorization': f'Bearer {admin_token}'}
                response = requests.get(f"{BASE_URL}/admin", headers=headers)
                if response.status_code == 200:
                    print("✅ Admin dashboard accessible")
                else:
                    print("❌ Admin dashboard not accessible")
            except Exception as e:
                print(f"❌ Admin dashboard error: {e}")
            
            # Test 8: Admin API Endpoints
            print("\n8. Testing Admin API Endpoints...")
            try:
                # Test admin stats
                response = requests.get(f"{BASE_URL}/api/admin/stats", headers=headers)
                if response.status_code == 200:
                    print("✅ Admin stats API working")
                else:
                    print("❌ Admin stats API failed")
                
                # Test admin users
                response = requests.get(f"{BASE_URL}/api/admin/users", headers=headers)
                if response.status_code == 200:
                    print("✅ Admin users API working")
                else:
                    print("❌ Admin users API failed")
                
                # Test admin packages
                response = requests.get(f"{BASE_URL}/api/admin/packages", headers=headers)
                if response.status_code == 200:
                    print("✅ Admin packages API working")
                else:
                    print("❌ Admin packages API failed")
                
            except Exception as e:
                print(f"❌ Admin API error: {e}")
            
        else:
            print("❌ Admin login failed")
            
    except Exception as e:
        print(f"❌ Admin login error: {e}")
    
    # Test 9: Navigation Authentication
    print("\n9. Testing Navigation Authentication...")
    try:
        # Test home page with authentication
        headers = {'Authorization': f'Bearer {auth_token}'}
        response = requests.get(f"{BASE_URL}/", headers=headers)
        if response.status_code == 200:
            print("✅ Home page with authentication works")
        else:
            print("❌ Home page with authentication failed")
    except Exception as e:
        print(f"❌ Navigation authentication error: {e}")
    
    # Test 10: Package Pages
    print("\n10. Testing Package Pages...")
    try:
        # Test packages page
        response = requests.get(f"{BASE_URL}/packages")
        if response.status_code == 200:
            print("✅ Packages page loads successfully")
        else:
            print("❌ Packages page failed to load")
        
        # Test package detail page
        response = requests.get(f"{BASE_URL}/package/1")
        if response.status_code == 200:
            print("✅ Package detail page loads successfully")
        else:
            print("❌ Package detail page failed to load")
            
    except Exception as e:
        print(f"❌ Package pages error: {e}")
    
    print("\n" + "=" * 60)
    print("NEW FEATURES TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    print("Testing new features...")
    print("Make sure the Flask application is running on http://localhost:5000")
    time.sleep(2)
    test_new_features()
