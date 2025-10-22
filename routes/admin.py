from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, TravelPackage, Booking, Review, UserRole, BookingStatus
from datetime import datetime, date, timedelta
import json

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to check if user is admin"""
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != UserRole.ADMIN:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        role = request.args.get('role')
        search = request.args.get('search', '')
        
        # Build query
        query = User.query
        
        if role:
            try:
                role_enum = UserRole(role)
                query = query.filter_by(role=role_enum)
            except ValueError:
                return jsonify({'error': 'Invalid role'}), 400
        
        if search:
            query = query.filter(
                (User.username.ilike(f'%{search}%')) |
                (User.email.ilike(f'%{search}%'))
            )
        
        # Paginate results
        users = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        user_list = [user.to_dict() for user in users.items]
        
        return jsonify({
            'users': user_list,
            'total': users.total,
            'pages': users.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'username' in data:
            # Check if username is already taken
            existing_user = User.query.filter(User.username == data['username'], User.id != user_id).first()
            if existing_user:
                return jsonify({'error': 'Username already exists'}), 400
            user.username = data['username']
        
        if 'email' in data:
            # Check if email is already taken
            existing_user = User.query.filter(User.email == data['email'], User.id != user_id).first()
            if existing_user:
                return jsonify({'error': 'Email already exists'}), 400
            user.email = data['email']
        
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        
        if 'role' in data:
            try:
                user.role = UserRole(data['role'])
            except ValueError:
                return jsonify({'error': 'Invalid role'}), 400
        
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@jwt_required()
@admin_required
def deactivate_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'User deactivated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>/activate', methods=['POST'])
@jwt_required()
@admin_required
def activate_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = True
        db.session.commit()
        
        return jsonify({'message': 'User activated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/packages', methods=['GET'])
@jwt_required()
@admin_required
def get_all_packages():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        destination = request.args.get('destination', '')
        is_active = request.args.get('is_active')
        
        # Build query
        query = TravelPackage.query
        
        if destination:
            query = query.filter(TravelPackage.destination.ilike(f'%{destination}%'))
        
        if is_active is not None:
            query = query.filter_by(is_active=is_active.lower() == 'true')
        
        # Paginate results
        packages = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        package_list = [package.to_dict() for package in packages.items]
        
        return jsonify({
            'packages': package_list,
            'total': packages.total,
            'pages': packages.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/bookings', methods=['GET'])
@jwt_required()
@admin_required
def get_all_bookings():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        user_id = request.args.get('user_id', type=int)
        package_id = request.args.get('package_id', type=int)
        
        # Build query
        query = Booking.query
        
        if status:
            try:
                status_enum = BookingStatus(status)
                query = query.filter_by(status=status_enum)
            except ValueError:
                return jsonify({'error': 'Invalid status'}), 400
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if package_id:
            query = query.filter_by(package_id=package_id)
        
        # Paginate results
        bookings = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        booking_list = [booking.to_dict() for booking in bookings.items]
        
        return jsonify({
            'bookings': booking_list,
            'total': bookings.total,
            'pages': bookings.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/bookings/<int:booking_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_booking_status(booking_id):
    try:
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        data = request.get_json()
        
        if 'status' not in data:
            return jsonify({'error': 'Status is required'}), 400
        
        try:
            booking.status = BookingStatus(data['status'])
        except ValueError:
            return jsonify({'error': 'Invalid status'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking status updated successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_stats():
    try:
        # Get statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        total_packages = TravelPackage.query.count()
        active_packages = TravelPackage.query.filter_by(is_active=True).count()
        total_bookings = Booking.query.count()
        pending_bookings = Booking.query.filter_by(status=BookingStatus.PENDING).count()
        confirmed_bookings = Booking.query.filter_by(status=BookingStatus.CONFIRMED).count()
        completed_bookings = Booking.query.filter_by(status=BookingStatus.COMPLETED).count()
        cancelled_bookings = Booking.query.filter_by(status=BookingStatus.CANCELLED).count()
        total_reviews = Review.query.count()
        
        # Calculate total revenue
        completed_bookings_query = Booking.query.filter_by(status=BookingStatus.COMPLETED)
        total_revenue = sum(booking.total_amount for booking in completed_bookings_query.all())
        
        # Get recent bookings (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_bookings = Booking.query.filter(Booking.created_at >= thirty_days_ago).count()
        
        return jsonify({
            'users': {
                'total': total_users,
                'active': active_users,
                'inactive': total_users - active_users
            },
            'packages': {
                'total': total_packages,
                'active': active_packages,
                'inactive': total_packages - active_packages
            },
            'bookings': {
                'total': total_bookings,
                'pending': pending_bookings,
                'confirmed': confirmed_bookings,
                'completed': completed_bookings,
                'cancelled': cancelled_bookings,
                'recent_30_days': recent_bookings
            },
            'reviews': {
                'total': total_reviews
            },
            'revenue': {
                'total': total_revenue
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/reviews', methods=['GET'])
@jwt_required()
@admin_required
def get_all_reviews():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        package_id = request.args.get('package_id', type=int)
        user_id = request.args.get('user_id', type=int)
        
        # Build query
        query = Review.query
        
        if package_id:
            query = query.filter_by(package_id=package_id)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        # Paginate results
        reviews = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        review_list = [review.to_dict() for review in reviews.items]
        
        return jsonify({
            'reviews': review_list,
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
