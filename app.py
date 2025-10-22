from flask import Flask, request, jsonify, render_template
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_mail import Mail
from datetime import datetime, timedelta
import os
import urllib.parse
import requests
from dotenv import load_dotenv
from database import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
mysql_password = urllib.parse.quote_plus(os.getenv('MYSQL_PASSWORD', 'Harsha@9625'))
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{mysql_password}@localhost/tourism_management"
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
from routes.admin import admin_bp
from routes.payments import payments_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(packages_bp, url_prefix='/api/packages')
app.register_blueprint(bookings_bp, url_prefix='/api/bookings')
app.register_blueprint(reviews_bp, url_prefix='/api/reviews')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(payments_bp, url_prefix='/api/payments')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/packages')
def packages():
    return render_template('packages.html')

@app.route('/package/<int:package_id>')
def package_detail(package_id):
    try:
        # Get package details directly from database
        package = TravelPackage.query.get(package_id)
        if not package or not package.is_active:
            return "Package not found", 404
        
        # Add average rating
        reviews = Review.query.filter_by(package_id=package_id).all()
        if reviews:
            avg_rating = sum(review.rating for review in reviews) / len(reviews)
            package.average_rating = round(avg_rating, 1)
            package.total_reviews = len(reviews)
        else:
            package.average_rating = 0
            package.total_reviews = 0
        
        return render_template('package_detail.html', package=package)
    except Exception as e:
        return f"Error loading package: {str(e)}", 500

@app.route('/admin')
@jwt_required()
def admin_panel():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != UserRole.ADMIN:
        return "Access denied", 403
    
    return render_template('admin.html', current_user=user)

@app.route('/bookings')
@jwt_required()
def bookings():
    return render_template('bookings.html')

@app.route('/profile')
@jwt_required()
def profile():
    return render_template('profile.html')

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
