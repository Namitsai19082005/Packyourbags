#!/usr/bin/env python3
"""
Development Mode Runner
Runs both React frontend (port 3000) and Flask backend (port 5000) separately
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def run_backend():
    """Run the Flask backend server"""
    print("🚀 Starting Flask backend on http://localhost:5000")
    os.system("python app_sqlite.py")

def run_frontend():
    """Run the React frontend development server"""
    print("⚛️  Starting React frontend on http://localhost:3000")
    os.chdir("frontend")
    os.system("npm start")

def main():
    """Main function to run both servers"""
    print("=" * 60)
    print("🌍 TOURISM MANAGEMENT SYSTEM - DEVELOPMENT MODE")
    print("=" * 60)
    print("This will start:")
    print("  • Flask Backend: http://localhost:5000")
    print("  • React Frontend: http://localhost:3000")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("app_sqlite.py"):
        print("✗ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if frontend directory exists
    if not os.path.exists("frontend"):
        print("✗ Frontend directory not found")
        sys.exit(1)
    
    # Check if node_modules exists
    if not os.path.exists("frontend/node_modules"):
        print("📦 Installing frontend dependencies...")
        os.chdir("frontend")
        os.system("npm install")
        os.chdir("..")
    
    print("\n🚀 Starting servers...")
    print("Press Ctrl+C to stop both servers")
    print("-" * 50)
    
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()
        
        # Wait a moment for backend to start
        time.sleep(2)
        
        # Start frontend (this will block)
        run_frontend()
        
    except KeyboardInterrupt:
        print("\n✓ Servers stopped")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()
