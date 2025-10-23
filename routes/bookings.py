from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Booking, TravelPackage, User, UserRole, BookingStatus
from datetime import datetime, date
import json

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['package_id', 'booking_date', 'number_of_travelers']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if package exists and is active
        package = TravelPackage.query.get(data['package_id'])
        if not package or not package.is_active:
            return jsonify({'error': 'Package not found or inactive'}), 404
        
        # Validate booking date
        try:
            booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid booking_date format. Use YYYY-MM-DD'}), 400
        
        # Check if booking date is within package availability
        if booking_date < package.available_from or booking_date > package.available_to:
            return jsonify({'error': 'Booking date is outside package availability'}), 400
        
        # Check if booking date is not in the past
        if booking_date < date.today():
            return jsonify({'error': 'Cannot book for past dates'}), 400
        
        # Validate number of travelers
        if data['number_of_travelers'] > package.max_travelers:
            return jsonify({'error': f'Maximum {package.max_travelers} travelers allowed'}), 400
        
        if data['number_of_travelers'] <= 0:
            return jsonify({'error': 'Number of travelers must be greater than 0'}), 400
        
        # Calculate total amount
        total_amount = package.price * data['number_of_travelers']
        
        # Create booking
        booking = Booking(
            user_id=user_id,
            package_id=data['package_id'],
            booking_date=booking_date,
            number_of_travelers=data['number_of_travelers'],
            total_amount=total_amount,
            special_requests=data.get('special_requests', '')
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return jsonify({
            'message': 'Booking created successfully',
            'booking': booking.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_bookings():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        # Build query
        query = Booking.query.filter_by(user_id=user_id)
        
        if status:
            try:
                status_enum = BookingStatus(status)
                query = query.filter_by(status=status_enum)
            except ValueError:
                return jsonify({'error': 'Invalid status'}), 400
        
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

@bookings_bp.route('/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if user owns the booking or is admin/travel agent
        if booking.user_id != user_id and user.role not in [UserRole.ADMIN, UserRole.TRAVEL_AGENT]:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'success': True,
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/<int:booking_id>', methods=['PUT'])
@jwt_required()
def update_booking(booking_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if user owns the booking or is admin/travel agent
        if booking.user_id != user_id and user.role not in [UserRole.ADMIN, UserRole.TRAVEL_AGENT]:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'special_requests' in data:
            booking.special_requests = data['special_requests']
        
        # Only admin and travel agents can change status
        if 'status' in data and user.role in [UserRole.ADMIN, UserRole.TRAVEL_AGENT]:
            try:
                booking.status = BookingStatus(data['status'])
            except ValueError:
                return jsonify({'error': 'Invalid status'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Booking updated successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if user owns the booking or is admin/travel agent
        if booking.user_id != user_id and user.role not in [UserRole.ADMIN, UserRole.TRAVEL_AGENT]:
            return jsonify({'error': 'Access denied'}), 403
        
        # Check if booking can be cancelled
        if booking.status == BookingStatus.CANCELLED:
            return jsonify({'error': 'Booking is already cancelled'}), 400
        
        if booking.status == BookingStatus.COMPLETED:
            return jsonify({'error': 'Cannot cancel completed booking'}), 400
        
        # Cancel booking
        booking.status = BookingStatus.CANCELLED
        db.session.commit()
        
        return jsonify({
            'message': 'Booking cancelled successfully',
            'booking': booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bookings_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_bookings():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Check if user is admin or travel agent
        if user.role not in [UserRole.ADMIN, UserRole.TRAVEL_AGENT]:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        user_filter = request.args.get('user_id', type=int)
        
        # Build query
        query = Booking.query
        
        if status:
            try:
                status_enum = BookingStatus(status)
                query = query.filter_by(status=status_enum)
            except ValueError:
                return jsonify({'error': 'Invalid status'}), 400
        
        if user_filter:
            query = query.filter_by(user_id=user_filter)
        
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
