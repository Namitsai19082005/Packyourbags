#!/usr/bin/env python3
"""
Tourism Management System - Complete System Runner
This script initializes the database and starts the Flask backend server.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_jwt_extended
        import flask_cors
        print("✓ All Python requirements are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing Python package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def initialize_database():
    """Initialize the database with sample data"""
    print("Initializing database...")
    try:
        from init_db_sqlite import init_database
        init_database()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False

def start_backend():
    """Start the Flask backend server"""
    print("Starting Flask backend server...")
    print("Backend will be available at: http://localhost:5000")
    print("API endpoints will be available at: http://localhost:5000/api/")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Use the SQLite version for easier setup
        os.system("python app_sqlite.py")
    except KeyboardInterrupt:
        print("\n✓ Server stopped")
    except Exception as e:
        print(f"✗ Server error: {e}")

def main():
    """Main function to run the complete system"""
    print("=" * 60)
    print("🌍 TOURISM MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app_sqlite.py"):
        print("✗ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        sys.exit(1)
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    main()
