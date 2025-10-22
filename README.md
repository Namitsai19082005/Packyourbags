# Tourism Management System - "Pack Your Bags"

A comprehensive web-based tourism management system built with Flask backend and modern frontend technologies.

## Features

### User Management
- User registration and authentication
- JWT-based secure authentication
- Role-based access control (End User, Travel Agent, Admin)
- Profile management

### Travel Package Management
- Search and filter travel packages
- Package details with images and descriptions
- Price and availability management
- Package reviews and ratings

### Booking System
- Create and manage travel bookings
- Booking status tracking
- Payment integration with Razorpay
- Booking history and management

### Review System
- Customer reviews and ratings
- Review management for admins
- Average rating calculation

### Admin Dashboard
- User management
- Package management
- Booking management
- Payment tracking
- System statistics

### Payment Integration
- Razorpay payment gateway integration
- Secure payment processing
- Payment verification
- Refund management

## Technology Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **MySQL** - Database
- **JWT** - Authentication
- **Razorpay** - Payment processing
- **Flask-Mail** - Email notifications

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - UI framework
- **JavaScript** - Interactive functionality
- **Font Awesome** - Icons

## Installation and Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd tourism-management-system
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
1. Create a MySQL database named `tourism_management`
2. Update the database connection in `app.py` if needed
3. Run the database initialization script:
```bash
python init_db.py
```

### 4. Environment Configuration
Create a `.env` file in the root directory with the following variables:
```env
# Database Configuration
MYSQL_PASSWORD=Harsha@9625

# JWT Configuration
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-string-change-in-production

# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Razorpay Configuration
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
```

### 5. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get user profile
- `PUT /api/auth/profile` - Update user profile
- `POST /api/auth/change-password` - Change password

### Travel Packages
- `GET /api/packages` - Get all packages (with filters)
- `GET /api/packages/<id>` - Get package details
- `POST /api/packages` - Create package (Admin/Travel Agent)
- `PUT /api/packages/<id>` - Update package (Admin/Travel Agent)
- `DELETE /api/packages/<id>` - Delete package (Admin)
- `GET /api/packages/destinations` - Get all destinations

### Bookings
- `POST /api/bookings` - Create booking
- `GET /api/bookings` - Get user bookings
- `GET /api/bookings/<id>` - Get booking details
- `PUT /api/bookings/<id>` - Update booking
- `POST /api/bookings/<id>/cancel` - Cancel booking
- `GET /api/bookings/all` - Get all bookings (Admin/Travel Agent)

### Reviews
- `POST /api/reviews` - Create review
- `GET /api/reviews/package/<id>` - Get package reviews
- `GET /api/reviews/<id>` - Get review details
- `PUT /api/reviews/<id>` - Update review
- `DELETE /api/reviews/<id>` - Delete review
- `GET /api/reviews/user` - Get user reviews
- `GET /api/reviews/all` - Get all reviews (Admin)

### Payments
- `POST /api/payments/create-order` - Create payment order
- `POST /api/payments/verify` - Verify payment
- `GET /api/payments/status/<id>` - Get payment status
- `GET /api/payments/booking/<id>` - Get booking payments
- `POST /api/payments/refund` - Create refund (Admin)
- `GET /api/payments/all` - Get all payments (Admin)

### Admin
- `GET /api/admin/users` - Get all users
- `GET /api/admin/users/<id>` - Get user details
- `PUT /api/admin/users/<id>` - Update user
- `POST /api/admin/users/<id>/deactivate` - Deactivate user
- `POST /api/admin/users/<id>/activate` - Activate user
- `GET /api/admin/packages` - Get all packages
- `GET /api/admin/bookings` - Get all bookings
- `PUT /api/admin/bookings/<id>/status` - Update booking status
- `GET /api/admin/stats` - Get system statistics
- `GET /api/admin/reviews` - Get all reviews

## Database Schema

### Users Table
- id, username, email, phone_number, password_hash, role, is_active, created_at, updated_at

### Travel Packages Table
- id, title, description, destination, duration_days, price, max_travelers, available_from, available_to, includes, excludes, images, is_active, created_at, updated_at

### Bookings Table
- id, user_id, package_id, booking_date, number_of_travelers, total_amount, status, special_requests, created_at, updated_at

### Reviews Table
- id, user_id, package_id, rating, comment, created_at, updated_at

### Payments Table
- id, booking_id, razorpay_payment_id, razorpay_order_id, amount, currency, status, payment_method, created_at, updated_at

### Itineraries Table
- id, booking_id, day_number, title, description, activities, accommodation, meals, created_at, updated_at

## Default Admin Account
- **Username:** admin
- **Password:** admin123
- **Email:** admin@tourism.com

## Sample Data
The system comes with 6 sample travel packages:
1. Paris City Break
2. Tokyo Adventure
3. Santorini Sunset Experience
4. New York City Explorer
5. Bali Tropical Paradise
6. Dubai Luxury Experience

## Security Features
- JWT-based authentication
- Password hashing with bcrypt
- Input validation and sanitization
- SQL injection prevention
- CORS configuration
- Role-based access control

## Performance Requirements
- Handles up to 500 concurrent users
- Response time under 2 seconds for most operations
- Scalable to 1,000 concurrent users
- 99.9% uptime target

## Development Notes
- The frontend is minimal and designed for testing the backend APIs
- React frontend can be integrated later
- All API endpoints are RESTful
- Comprehensive error handling
- Detailed logging for debugging

## Future Enhancements
- Real-time notifications
- Advanced search and filtering
- Mobile app integration
- Social media integration
- Advanced analytics dashboard
- Multi-language support

## Support
For technical support or questions, please contact the development team.

## License
This project is proprietary software developed for educational purposes.
