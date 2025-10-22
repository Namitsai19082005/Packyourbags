#!/usr/bin/env python3
"""
Setup script for Tourism Management System
"""

import os
import sys
import subprocess

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("Installing mysql-connector-python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
    import mysql.connector
    from mysql.connector import Error

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"[OK] Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[OK] Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def create_database():
    """Create MySQL database"""
    print("Creating MySQL database...")
    
    # Get database credentials
    db_password = input("Enter MySQL password (default: Harsha@9625): ").strip()
    if not db_password:
        db_password = "Harsha@9625"
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=db_password
        )
        
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS tourism_management")
        print("[OK] Database 'tourism_management' created")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"Error creating database: {e}")
        print("Please make sure MySQL is running and the password is correct")
        sys.exit(1)

def create_env_file():
    """Create .env file with configuration"""
    print("Creating environment configuration...")
    
    env_content = f"""# Database Configuration
MYSQL_PASSWORD=Harsha@9625

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production-{os.urandom(16).hex()}
JWT_SECRET_KEY=jwt-secret-string-change-in-production-{os.urandom(16).hex()}

# Email Configuration (Optional - for email notifications)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Razorpay Configuration (Required for payments)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("[OK] Environment file created (.env)")
    print("[WARNING] Please update the .env file with your actual API keys")

def initialize_database():
    """Initialize database with tables and sample data"""
    print("Initializing database...")
    try:
        subprocess.check_call([sys.executable, "init_db.py"])
        print("[OK] Database initialized with sample data")
    except subprocess.CalledProcessError as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

def main():
    """Main setup function"""
    print("=" * 50)
    print("Tourism Management System Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create database
    create_database()
    
    # Create environment file
    create_env_file()
    
    # Initialize database
    initialize_database()
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Update the .env file with your API keys:")
    print("   - Razorpay Key ID and Secret (for payments)")
    print("   - Email credentials (for notifications)")
    print("\n2. Run the application:")
    print("   python app.py")
    print("\n3. Access the application:")
    print("   http://localhost:5000")
    print("\n4. Default admin login:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n5. API documentation available at:")
    print("   http://localhost:5000/api/health")

if __name__ == "__main__":
    main()
