from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from database import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration - Using SQLite for easy testing
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tourism_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Razorpay configuration
app.config['RAZORPAY_KEY_ID'] = os.getenv('RAZORPAY_KEY_ID')
app.config['RAZORPAY_KEY_SECRET'] = os.getenv('RAZORPAY_KEY_SECRET')

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
cors = CORS(app)
mail = Mail(app)

# Import models and routes
from models import *
from routes.auth import auth_bp
from routes.packages import packages_bp
from routes.bookings import bookings_bp
from routes.reviews import reviews_bp
from routes.itineraries import itineraries_bp
from routes.admin import admin_bp
from routes.payments import payments_bp
from routes.wishlist import wishlist_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(packages_bp, url_prefix='/api/packages')
app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
app.register_blueprint(itineraries_bp, url_prefix='/api/itineraries')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(payments_bp, url_prefix='/api/payments')
app.register_blueprint(wishlist_bp, url_prefix='/api/wishlist')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/packages')
def packages_page():
    return render_template('packages.html')

@app.route('/bookings')
def bookings_page():
    return render_template('bookings.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/admin-profile')
def admin_profile_page():
    return render_template('admin_dashboard.html')

@app.route('/admin-profile-page')
def admin_profile_page_new():
    return render_template('admin_profile.html')

@app.route('/package/<int:package_id>')
def package_detail_page(package_id):
    return render_template('package_detail.html')

@app.route('/wishlist')
def wishlist_page():
    return render_template('wishlist.html')

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
