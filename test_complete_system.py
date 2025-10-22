#!/usr/bin/env python3
"""
Complete System Test for Tourism Management System
Tests all major functionalities end-to-end
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

class TourismSystemTester:
    def __init__(self):
        self.auth_token = None
        self.admin_token = None
        self.test_user_id = None
        self.test_package_id = None
        self.test_booking_id = None
        self.test_review_id = None
        
    def run_all_tests(self):
        """Run all system tests"""
        print("=" * 60)
        print("TOURISM MANAGEMENT SYSTEM - COMPLETE TEST SUITE")
        print("=" * 60)
        
        tests = [
            ("Health Check", self.test_health),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Admin Login", self.test_admin_login),
            ("Get Packages", self.test_get_packages),
            ("Get Package Details", self.test_get_package_details),
            ("Create Booking", self.test_create_booking),
            ("Get User Bookings", self.test_get_user_bookings),
            ("Create Review", self.test_create_review),
            ("Get Package Reviews", self.test_get_package_reviews),
            ("Admin Dashboard Stats", self.test_admin_stats),
            ("Admin User Management", self.test_admin_users),
            ("Admin Package Management", self.test_admin_packages),
            ("Admin Booking Management", self.test_admin_bookings),
            ("Payment Integration", self.test_payment_integration),
            ("Search and Filter", self.test_search_filter),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_func()
                if result:
                    print(f"✅ {test_name} - PASSED")
                    passed += 1
                else:
                    print(f"❌ {test_name} - FAILED")
                    failed += 1
            except Exception as e:
                print(f"❌ {test_name} - ERROR: {str(e)}")
                failed += 1
        
        print("\n" + "=" * 60)
        print(f"TEST RESULTS: {passed} PASSED, {failed} FAILED")
        print("=" * 60)
        
        return failed == 0
    
    def test_health(self):
        """Test health endpoint"""
        response = requests.get(f"{BASE_URL}/api/health")
        return response.status_code == 200
    
    def test_user_registration(self):
        """Test user registration"""
        user_data = {
            "username": "testuser123",
            "email": "testuser123@example.com",
            "phone_number": "+1234567890",
            "password": "testpass123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
        if response.status_code == 201:
            data = response.json()
            self.auth_token = data.get('access_token')
            self.test_user_id = data.get('user', {}).get('id')
            return True
        return False
    
    def test_user_login(self):
        """Test user login"""
        login_data = {
            "username": "testuser123",
            "password": "testpass123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            self.auth_token = data.get('access_token')
            return True
        return False
    
    def test_admin_login(self):
        """Test admin login"""
        admin_data = {
            "username": "admin",
            "password": "admin123"
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", json=admin_data)
        if response.status_code == 200:
            data = response.json()
            self.admin_token = data.get('access_token')
            return True
        return False
    
    def test_get_packages(self):
        """Test getting packages"""
        response = requests.get(f"{BASE_URL}/api/packages")
        if response.status_code == 200:
            data = response.json()
            if data.get('packages') and len(data['packages']) > 0:
                self.test_package_id = data['packages'][0]['id']
                return True
        return False
    
    def test_get_package_details(self):
        """Test getting package details"""
        if not self.test_package_id:
            return False
            
        response = requests.get(f"{BASE_URL}/api/packages/{self.test_package_id}")
        if response.status_code == 200:
            data = response.json()
            return 'package' in data
        return False
    
    def test_create_booking(self):
        """Test creating a booking"""
        if not self.auth_token or not self.test_package_id:
            return False
            
        booking_data = {
            "package_id": self.test_package_id,
            "booking_date": "2024-12-25",
            "number_of_travelers": 2
        }
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        response = requests.post(f"{BASE_URL}/api/bookings", json=booking_data, headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            self.test_booking_id = data.get('booking', {}).get('id')
            return True
        return False
    
    def test_get_user_bookings(self):
        """Test getting user bookings"""
        if not self.auth_token:
            return False
            
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        response = requests.get(f"{BASE_URL}/api/bookings", headers=headers)
        return response.status_code == 200
    
    def test_create_review(self):
        """Test creating a review"""
        if not self.auth_token or not self.test_package_id:
            return False
            
        # First, we need to complete the booking to be able to review
        # For testing purposes, we'll simulate this by updating booking status
        if self.test_booking_id and self.admin_token:
            # Update booking status to completed
            headers = {'Authorization': f'Bearer {self.admin_token}'}
            update_data = {"status": "completed"}
            requests.put(f"{BASE_URL}/api/admin/bookings/{self.test_booking_id}/status", 
                        json=update_data, headers=headers)
        
        review_data = {
            "package_id": self.test_package_id,
            "rating": 5,
            "comment": "Excellent package! Highly recommended."
        }
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        response = requests.post(f"{BASE_URL}/api/reviews", json=review_data, headers=headers)
        
        if response.status_code == 201:
            data = response.json()
            self.test_review_id = data.get('review', {}).get('id')
            return True
        return False
    
    def test_get_package_reviews(self):
        """Test getting package reviews"""
        if not self.test_package_id:
            return False
            
        response = requests.get(f"{BASE_URL}/api/reviews/package/{self.test_package_id}")
        return response.status_code == 200
    
    def test_admin_stats(self):
        """Test admin statistics"""
        if not self.admin_token:
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = requests.get(f"{BASE_URL}/api/admin/stats", headers=headers)
        return response.status_code == 200
    
    def test_admin_users(self):
        """Test admin user management"""
        if not self.admin_token:
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = requests.get(f"{BASE_URL}/api/admin/users", headers=headers)
        return response.status_code == 200
    
    def test_admin_packages(self):
        """Test admin package management"""
        if not self.admin_token:
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = requests.get(f"{BASE_URL}/api/admin/packages", headers=headers)
        return response.status_code == 200
    
    def test_admin_bookings(self):
        """Test admin booking management"""
        if not self.admin_token:
            return False
            
        headers = {'Authorization': f'Bearer {self.admin_token}'}
        response = requests.get(f"{BASE_URL}/api/admin/bookings", headers=headers)
        return response.status_code == 200
    
    def test_payment_integration(self):
        """Test payment integration"""
        if not self.auth_token or not self.test_booking_id:
            return False
            
        # Test creating payment order
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        payment_data = {"booking_id": self.test_booking_id}
        
        response = requests.post(f"{BASE_URL}/api/payments/create-order", 
                               json=payment_data, headers=headers)
        return response.status_code == 200
    
    def test_search_filter(self):
        """Test search and filter functionality"""
        # Test destination search
        response = requests.get(f"{BASE_URL}/api/packages?destination=Paris")
        if response.status_code != 200:
            return False
            
        # Test price filter
        response = requests.get(f"{BASE_URL}/api/packages?min_price=500&max_price=2000")
        if response.status_code != 200:
            return False
            
        # Test duration filter
        response = requests.get(f"{BASE_URL}/api/packages?duration=5")
        if response.status_code != 200:
            return False
            
        return True

def main():
    """Main test function"""
    print("Starting Tourism Management System Tests...")
    print("Make sure the Flask application is running on http://localhost:5000")
    
    # Wait a moment for user to read
    time.sleep(2)
    
    tester = TourismSystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! The system is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
