#!/usr/bin/env python3
"""
Database initialization script for Tourism Management System (SQLite version)
"""

from app_sqlite import app, db
from models import User, TravelPackage, UserRole
from datetime import datetime, date, timedelta
import json

def create_admin_user():
    """Create admin user if it doesn't exist"""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@tourism.com',
            phone_number='+1234567890',
            role=UserRole.ADMIN
        )
        admin.set_password('admin123')
        db.session.add(admin)
        print("Admin user created: username=admin, password=admin123")
    else:
        print("Admin user already exists")

def create_sample_packages():
    """Create sample travel packages"""
    packages = [
        {
            'title': 'Paris City Break',
            'description': 'Explore the romantic city of Paris with visits to Eiffel Tower, Louvre Museum, and Seine River cruise.',
            'destination': 'Paris, France',
            'duration_days': 5,
            'price': 1200.00,
            'max_travelers': 8,
            'available_from': date.today(),
            'available_to': date.today() + timedelta(days=365),
            'includes': ['Hotel accommodation', 'Breakfast', 'City tour', 'Museum tickets'],
            'excludes': ['International flights', 'Lunch and dinner', 'Personal expenses'],
            'images': ['https://images.unsplash.com/photo-1502602898536-47ad22581b52?w=500', 'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=500']
        },
        {
            'title': 'Tokyo Adventure',
            'description': 'Discover the vibrant culture of Tokyo with visits to temples, gardens, and modern districts.',
            'destination': 'Tokyo, Japan',
            'duration_days': 7,
            'price': 1800.00,
            'max_travelers': 6,
            'available_from': date.today(),
            'available_to': date.today() + timedelta(days=365),
            'includes': ['Hotel accommodation', 'Breakfast', 'JR Pass', 'Temple visits'],
            'excludes': ['International flights', 'Meals', 'Personal expenses'],
            'images': ['https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=500', 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=500']
        },
        {
            'title': 'Santorini Sunset Experience',
            'description': 'Relax in the beautiful Greek island of Santorini with stunning sunsets and white-washed buildings.',
            'destination': 'Santorini, Greece',
            'duration_days': 4,
            'price': 900.00,
            'max_travelers': 10,
            'available_from': date.today(),
            'available_to': date.today() + timedelta(days=365),
            'includes': ['Hotel accommodation', 'Breakfast', 'Sunset cruise', 'Wine tasting'],
            'excludes': ['International flights', 'Lunch and dinner', 'Personal expenses'],
            'images': ['https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=500', 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=500']
        },
        {
            'title': 'New York City Explorer',
            'description': 'Experience the Big Apple with visits to iconic landmarks, Broadway shows, and world-class dining.',
            'destination': 'New York, USA',
            'duration_days': 6,
            'price': 1500.00,
            'max_travelers': 8,
            'available_from': date.today(),
            'available_to': date.today() + timedelta(days=365),
            'includes': ['Hotel accommodation', 'Breakfast', 'Broadway show ticket', 'City pass'],
            'excludes': ['International flights', 'Lunch and dinner', 'Personal expenses'],
            'images': ['https://images.unsplash.com/photo-1496442226664-8d60ad3097cc?w=500', 'https://images.unsplash.com/photo-1485875437342-9b39470b3d95?w=500']
        },
        {
            'title': 'Bali Tropical Paradise',
            'description': 'Escape to the tropical paradise of Bali with beautiful beaches, temples, and cultural experiences.',
            'destination': 'Bali, Indonesia',
            'duration_days': 8,
            'price': 1000.00,
            'max_travelers': 12,
            'available_from': date.today(),
            'available_to': date.today() + timedelta(days=365),
            'includes': ['Resort accommodation', 'Breakfast', 'Temple tours', 'Beach activities'],
            'excludes': ['International flights', 'Lunch and dinner', 'Personal expenses'],
            'images': ['https://images.unsplash.com/photo-1537953773345-d172ccf13cf1?w=500', 'https://images.unsplash.com/photo-1518548418730-b8ae2c4e3a1e?w=500']
        },
        {
            'title': 'Dubai Luxury Experience',
            'description': 'Indulge in luxury in Dubai with visits to Burj Khalifa, Palm Jumeirah, and desert safaris.',
            'destination': 'Dubai, UAE',
            'duration_days': 5,
            'price': 2000.00,
            'max_travelers': 6,
            'available_from': date.today(),
            'available_to': date.today() + timedelta(days=365),
            'includes': ['5-star hotel', 'Breakfast', 'Burj Khalifa tickets', 'Desert safari'],
            'excludes': ['International flights', 'Lunch and dinner', 'Personal expenses'],
            'images': ['https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=500', 'https://images.unsplash.com/photo-1539650116574-75c0c6d73c6e?w=500']
        }
    ]
    
    for package_data in packages:
        existing = TravelPackage.query.filter_by(title=package_data['title']).first()
        if not existing:
            package = TravelPackage(
                title=package_data['title'],
                description=package_data['description'],
                destination=package_data['destination'],
                duration_days=package_data['duration_days'],
                price=package_data['price'],
                max_travelers=package_data['max_travelers'],
                available_from=package_data['available_from'],
                available_to=package_data['available_to'],
                includes=json.dumps(package_data['includes']),
                excludes=json.dumps(package_data['excludes']),
                images=json.dumps(package_data['images'])
            )
            db.session.add(package)
    
    print("Sample packages created")

def init_database():
    """Initialize the database with tables and sample data"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created")
        
        # Create admin user
        create_admin_user()
        
        # Create sample packages
        create_sample_packages()
        
        # Commit all changes
        db.session.commit()
        print("Database initialization completed successfully!")

if __name__ == '__main__':
    init_database()
