from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Itinerary, Booking, User
from datetime import datetime
import json

itineraries_bp = Blueprint('itineraries', __name__)

@itineraries_bp.route('/booking/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking_itineraries(booking_id):
    try:
        user_id = get_jwt_identity()
        
        # Check if booking exists and belongs to user
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if user owns the booking or is admin
        user = User.query.get(user_id)
        if booking.user_id != user_id and user.role.value != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get itineraries for the booking
        itineraries = Itinerary.query.filter_by(booking_id=booking_id).order_by(Itinerary.day_number).all()
        
        itinerary_list = [itinerary.to_dict() for itinerary in itineraries]
        
        return jsonify({
            'success': True,
            'itineraries': itinerary_list
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@itineraries_bp.route('/booking/<int:booking_id>', methods=['POST'])
@jwt_required()
def create_itinerary(booking_id):
    try:
        user_id = get_jwt_identity()
        
        # Check if booking exists and belongs to user
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if user owns the booking or is admin
        user = User.query.get(user_id)
        if booking.user_id != user_id and user.role.value != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('day_number') or not data.get('title'):
            return jsonify({'error': 'Day number and title are required'}), 400
        
        # Parse activities if provided
        activities = []
        if data.get('activities'):
            if isinstance(data['activities'], str):
                try:
                    activities = json.loads(data['activities'])
                except json.JSONDecodeError:
                    activities = [data['activities']]
            elif isinstance(data['activities'], list):
                activities = data['activities']
        
        # Create new itinerary
        itinerary = Itinerary(
            booking_id=booking_id,
            day_number=data['day_number'],
            title=data['title'],
            description=data.get('description', ''),
            activities=json.dumps(activities) if activities else None,
            accommodation=data.get('accommodation', ''),
            meals=data.get('meals', '')
        )
        
        db.session.add(itinerary)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Itinerary created successfully',
            'itinerary': itinerary.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@itineraries_bp.route('/<int:itinerary_id>', methods=['PUT'])
@jwt_required()
def update_itinerary(itinerary_id):
    try:
        user_id = get_jwt_identity()
        
        # Get itinerary
        itinerary = Itinerary.query.get(itinerary_id)
        if not itinerary:
            return jsonify({'error': 'Itinerary not found'}), 404
        
        # Check if user owns the booking or is admin
        user = User.query.get(user_id)
        if itinerary.booking.user_id != user_id and user.role.value != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Update fields
        if 'day_number' in data:
            itinerary.day_number = data['day_number']
        if 'title' in data:
            itinerary.title = data['title']
        if 'description' in data:
            itinerary.description = data['description']
        if 'accommodation' in data:
            itinerary.accommodation = data['accommodation']
        if 'meals' in data:
            itinerary.meals = data['meals']
        if 'activities' in data:
            activities = data['activities']
            if isinstance(activities, str):
                try:
                    activities = json.loads(activities)
                except json.JSONDecodeError:
                    activities = [activities]
            elif isinstance(activities, list):
                activities = activities
            itinerary.activities = json.dumps(activities) if activities else None
        
        itinerary.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Itinerary updated successfully',
            'itinerary': itinerary.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@itineraries_bp.route('/<int:itinerary_id>', methods=['DELETE'])
@jwt_required()
def delete_itinerary(itinerary_id):
    try:
        user_id = get_jwt_identity()
        
        # Get itinerary
        itinerary = Itinerary.query.get(itinerary_id)
        if not itinerary:
            return jsonify({'error': 'Itinerary not found'}), 404
        
        # Check if user owns the booking or is admin
        user = User.query.get(user_id)
        if itinerary.booking.user_id != user_id and user.role.value != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(itinerary)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Itinerary deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
