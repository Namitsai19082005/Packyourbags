from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, TravelPackage, User, UserRole, Review
from datetime import datetime, date
import json

packages_bp = Blueprint('packages', __name__)

@packages_bp.route('/', methods=['GET'])
def get_packages():
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        destination = request.args.get('destination', '')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        duration = request.args.get('duration', type=int)
        available_from = request.args.get('available_from')
        available_to = request.args.get('available_to')
        
        # Build query
        query = TravelPackage.query.filter_by(is_active=True)
        
        if destination:
            query = query.filter(TravelPackage.destination.ilike(f'%{destination}%'))
        
        if min_price is not None:
            query = query.filter(TravelPackage.price >= min_price)
        
        if max_price is not None:
            query = query.filter(TravelPackage.price <= max_price)
        
        if duration:
            query = query.filter(TravelPackage.duration_days == duration)
        
        if available_from:
            try:
                from_date = datetime.strptime(available_from, '%Y-%m-%d').date()
                query = query.filter(TravelPackage.available_from <= from_date)
            except ValueError:
                return jsonify({'error': 'Invalid available_from date format. Use YYYY-MM-DD'}), 400
        
        if available_to:
            try:
                to_date = datetime.strptime(available_to, '%Y-%m-%d').date()
                query = query.filter(TravelPackage.available_to >= to_date)
            except ValueError:
                return jsonify({'error': 'Invalid available_to date format. Use YYYY-MM-DD'}), 400
        
        # Paginate results
        packages = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Add average rating to each package
        package_list = []
        for package in packages.items:
            package_dict = package.to_dict()
            
            # Calculate average rating
            reviews = Review.query.filter_by(package_id=package.id).all()
            if reviews:
                avg_rating = sum(review.rating for review in reviews) / len(reviews)
                package_dict['average_rating'] = round(avg_rating, 1)
                package_dict['total_reviews'] = len(reviews)
            else:
                package_dict['average_rating'] = 0
                package_dict['total_reviews'] = 0
            
            package_list.append(package_dict)
        
        return jsonify({
            'packages': package_list,
            'total': packages.total,
            'pages': packages.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@packages_bp.route('/<int:package_id>', methods=['GET'])
def get_package(package_id):
    try:
        package = TravelPackage.query.get(package_id)
        
        if not package or not package.is_active:
            return jsonify({'error': 'Package not found'}), 404
        
        package_dict = package.to_dict()
        
        # Add reviews and ratings
        reviews = Review.query.filter_by(package_id=package_id).all()
        if reviews:
            avg_rating = sum(review.rating for review in reviews) / len(reviews)
            package_dict['average_rating'] = round(avg_rating, 1)
            package_dict['total_reviews'] = len(reviews)
            package_dict['reviews'] = [review.to_dict() for review in reviews]
        else:
            package_dict['average_rating'] = 0
            package_dict['total_reviews'] = 0
            package_dict['reviews'] = []
        
        return jsonify({'package': package_dict}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@packages_bp.route('/', methods=['POST'])
@jwt_required()
def create_package():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Check if user is admin or travel agent
        if user.role not in [UserRole.ADMIN, UserRole.TRAVEL_AGENT]:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'destination', 'duration_days', 'price', 'max_travelers', 'available_from', 'available_to']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate dates
        try:
            available_from = datetime.strptime(data['available_from'], '%Y-%m-%d').date()
            available_to = datetime.strptime(data['available_to'], '%Y-%m-%d').date()
            
            if available_from >= available_to:
                return jsonify({'error': 'available_from must be before available_to'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Create package
        package = TravelPackage(
            title=data['title'],
            description=data.get('description', ''),
            destination=data['destination'],
            duration_days=data['duration_days'],
            price=data['price'],
            max_travelers=data['max_travelers'],
            available_from=available_from,
            available_to=available_to,
            includes=json.dumps(data.get('includes', [])),
            excludes=json.dumps(data.get('excludes', [])),
            images=json.dumps(data.get('images', []))
        )
        
        db.session.add(package)
        db.session.commit()
        
        return jsonify({
            'message': 'Package created successfully',
            'package': package.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@packages_bp.route('/<int:package_id>', methods=['PUT'])
@jwt_required()
def update_package(package_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Check if user is admin or travel agent
        if user.role not in [UserRole.ADMIN, UserRole.TRAVEL_AGENT]:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        package = TravelPackage.query.get(package_id)
        if not package:
            return jsonify({'error': 'Package not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            package.title = data['title']
        if 'description' in data:
            package.description = data['description']
        if 'destination' in data:
            package.destination = data['destination']
        if 'duration_days' in data:
            package.duration_days = data['duration_days']
        if 'price' in data:
            package.price = data['price']
        if 'max_travelers' in data:
            package.max_travelers = data['max_travelers']
        if 'available_from' in data:
            try:
                package.available_from = datetime.strptime(data['available_from'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid available_from date format. Use YYYY-MM-DD'}), 400
        if 'available_to' in data:
            try:
                package.available_to = datetime.strptime(data['available_to'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid available_to date format. Use YYYY-MM-DD'}), 400
        if 'includes' in data:
            package.includes = json.dumps(data['includes'])
        if 'excludes' in data:
            package.excludes = json.dumps(data['excludes'])
        if 'images' in data:
            package.images = json.dumps(data['images'])
        if 'is_active' in data:
            package.is_active = data['is_active']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Package updated successfully',
            'package': package.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@packages_bp.route('/<int:package_id>', methods=['DELETE'])
@jwt_required()
def delete_package(package_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Check if user is admin
        if user.role != UserRole.ADMIN:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        package = TravelPackage.query.get(package_id)
        if not package:
            return jsonify({'error': 'Package not found'}), 404
        
        # Soft delete by setting is_active to False
        package.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Package deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@packages_bp.route('/destinations', methods=['GET'])
def get_destinations():
    try:
        destinations = db.session.query(TravelPackage.destination).filter_by(is_active=True).distinct().all()
        destination_list = [dest[0] for dest in destinations]
        
        return jsonify({'destinations': destination_list}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
