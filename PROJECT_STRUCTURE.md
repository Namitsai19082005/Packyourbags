# Tourism Management System - Project Structure

```
tourism-management-system/
│
├── app.py                          # Main Flask application
├── models.py                       # Database models
├── init_db.py                      # Database initialization script
├── setup.py                        # Setup script for easy installation
├── test_api.py                     # API testing script
├── requirements.txt                # Python dependencies
├── env_example.txt                 # Environment variables example
├── README.md                       # Project documentation
├── PROJECT_STRUCTURE.md            # This file
│
├── routes/                         # API route modules
│   ├── __init__.py
│   ├── auth.py                     # Authentication routes
│   ├── packages.py                 # Travel package routes
│   ├── bookings.py                 # Booking management routes
│   ├── reviews.py                  # Review and rating routes
│   ├── admin.py                    # Admin dashboard routes
│   └── payments.py                 # Payment processing routes
│
└── templates/                      # Frontend templates
    └── index.html                  # Main frontend interface
```

## File Descriptions

### Core Application Files

- **`app.py`** - Main Flask application with configuration, database setup, and route registration
- **`models.py`** - SQLAlchemy database models for all entities (User, TravelPackage, Booking, Review, Payment, Itinerary)
- **`init_db.py`** - Database initialization script that creates tables and sample data
- **`setup.py`** - Automated setup script for easy installation and configuration
- **`test_api.py`** - Comprehensive API testing script to verify all endpoints

### Route Modules (`routes/`)

- **`auth.py`** - User authentication and profile management
  - User registration and login
  - JWT token management
  - Profile updates and password changes

- **`packages.py`** - Travel package management
  - Package search and filtering
  - CRUD operations for packages
  - Destination listing

- **`bookings.py`** - Booking management system
  - Create and manage bookings
  - Booking status updates
  - User booking history

- **`reviews.py`** - Review and rating system
  - Customer reviews and ratings
  - Review management
  - Average rating calculations

- **`admin.py`** - Administrative functions
  - User management
  - Package management
  - System statistics
  - Booking oversight

- **`payments.py`** - Payment processing
  - Razorpay integration
  - Payment verification
  - Refund management

### Frontend (`templates/`)

- **`index.html`** - Minimal frontend interface for testing backend functionality
  - Bootstrap 5 responsive design
  - User authentication forms
  - Package browsing interface
  - API integration examples

### Configuration Files

- **`requirements.txt`** - Python package dependencies
- **`env_example.txt`** - Environment variables template
- **`README.md`** - Comprehensive project documentation
- **`PROJECT_STRUCTURE.md`** - This file

## Database Schema

### Tables

1. **`users`** - User accounts and profiles
2. **`travel_packages`** - Travel package information
3. **`bookings`** - Travel bookings and reservations
4. **`reviews`** - Customer reviews and ratings
5. **`payments`** - Payment transactions
6. **`itineraries`** - Detailed travel itineraries

### Relationships

- Users have many Bookings and Reviews
- Travel Packages have many Bookings and Reviews
- Bookings have many Payments and Itineraries
- One-to-many relationships throughout the schema

## API Endpoints Overview

### Authentication (`/api/auth/`)
- POST `/register` - User registration
- POST `/login` - User login
- GET `/profile` - Get user profile
- PUT `/profile` - Update user profile
- POST `/change-password` - Change password

### Packages (`/api/packages/`)
- GET `/` - List packages with filters
- GET `/<id>` - Get package details
- POST `/` - Create package (Admin/Travel Agent)
- PUT `/<id>` - Update package (Admin/Travel Agent)
- DELETE `/<id>` - Delete package (Admin)
- GET `/destinations` - List all destinations

### Bookings (`/api/bookings/`)
- POST `/` - Create booking
- GET `/` - Get user bookings
- GET `/<id>` - Get booking details
- PUT `/<id>` - Update booking
- POST `/<id>/cancel` - Cancel booking
- GET `/all` - Get all bookings (Admin/Travel Agent)

### Reviews (`/api/reviews/`)
- POST `/` - Create review
- GET `/package/<id>` - Get package reviews
- GET `/<id>` - Get review details
- PUT `/<id>` - Update review
- DELETE `/<id>` - Delete review
- GET `/user` - Get user reviews
- GET `/all` - Get all reviews (Admin)

### Payments (`/api/payments/`)
- POST `/create-order` - Create payment order
- POST `/verify` - Verify payment
- GET `/status/<id>` - Get payment status
- GET `/booking/<id>` - Get booking payments
- POST `/refund` - Create refund (Admin)
- GET `/all` - Get all payments (Admin)

### Admin (`/api/admin/`)
- GET `/users` - Get all users
- GET `/users/<id>` - Get user details
- PUT `/users/<id>` - Update user
- POST `/users/<id>/deactivate` - Deactivate user
- POST `/users/<id>/activate` - Activate user
- GET `/packages` - Get all packages
- GET `/bookings` - Get all bookings
- PUT `/bookings/<id>/status` - Update booking status
- GET `/stats` - Get system statistics
- GET `/reviews` - Get all reviews

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Input validation and sanitization
- SQL injection prevention
- CORS configuration
- Role-based access control (End User, Travel Agent, Admin)

## Performance Considerations

- Database indexing on frequently queried fields
- Pagination for large result sets
- Efficient query patterns
- Connection pooling
- Response caching where appropriate

## Development Workflow

1. **Setup**: Run `python setup.py` for initial configuration
2. **Development**: Use `python app.py` to start the development server
3. **Testing**: Run `python test_api.py` to verify API functionality
4. **Database**: Use `python init_db.py` to reset database with sample data

## Deployment Notes

- Configure production environment variables
- Set up proper database credentials
- Configure Razorpay production keys
- Set up email service for notifications
- Configure proper CORS settings for production
- Use production WSGI server (e.g., Gunicorn)
- Set up reverse proxy (e.g., Nginx)
