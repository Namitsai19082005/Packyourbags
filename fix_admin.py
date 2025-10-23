#!/usr/bin/env python3
"""
Script to check and fix admin account status
"""

from app_sqlite import app, db
from models import User, UserRole

def check_and_fix_admin():
    """Check admin account status and fix if needed"""
    with app.app_context():
        # Check if admin exists
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            print(f"Admin account found:")
            print(f"  Username: {admin.username}")
            print(f"  Email: {admin.email}")
            print(f"  Role: {admin.role}")
            print(f"  Is Active: {admin.is_active}")
            print(f"  Created: {admin.created_at}")
            
            # If admin is not active, activate it
            if not admin.is_active:
                print("\n⚠️  Admin account is DEACTIVATED!")
                print("Activating admin account...")
                admin.is_active = True
                db.session.commit()
                print("✅ Admin account activated successfully!")
            else:
                print("\n✅ Admin account is already active")
                
            # Verify password
            if admin.check_password('admin123'):
                print("✅ Admin password is correct")
            else:
                print("❌ Admin password is incorrect")
                print("Resetting admin password...")
                admin.set_password('admin123')
                db.session.commit()
                print("✅ Admin password reset successfully!")
                
        else:
            print("❌ Admin account not found!")
            print("Creating admin account...")
            admin = User(
                username='admin',
                email='admin@tourism.com',
                phone_number='+1234567890',
                role=UserRole.ADMIN,
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin account created successfully!")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: admin@tourism.com")

if __name__ == "__main__":
    check_and_fix_admin()
