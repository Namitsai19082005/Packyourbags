from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Review, TravelPackage, User, UserRole, Booking, BookingStatus
from datetime import datetime

reviews_bp = Blueprint('reviews', __name__)

@reviews_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['package_id', 'rating']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate rating
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
        
        # Check if package exists
        package = TravelPackage.query.get(data['package_id'])
        if not package or not package.is_active:
            return jsonify({'error': 'Package not found or inactive'}), 404
        
        # Check if user has a completed booking for this package
        completed_booking = Booking.query.filter_by(
            user_id=user_id,
            package_id=data['package_id'],
            status=BookingStatus.COMPLETED
        ).first()
        
        if not completed_booking:
            return jsonify({'error': 'You can only review packages you have completed'}), 403
        
        # Check if user has already reviewed this package
        existing_review = Review.query.filter_by(
            user_id=user_id,
            package_id=data['package_id']
        ).first()
        
        if existing_review:
            return jsonify({'error': 'You have already reviewed this package'}), 400
        
        # Create review
        review = Review(
            user_id=user_id,
            package_id=data['package_id'],
            rating=rating,
            comment=data.get('comment', '')
        )
        
        db.session.add(review)
        db.session.commit()
        
        return jsonify({
            'message': 'Review created successfully',
            'review': review.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/package/<int:package_id>', methods=['GET'])
def get_package_reviews(package_id):
    try:
        # Check if package exists
        package = TravelPackage.query.get(package_id)
        if not package or not package.is_active:
            return jsonify({'error': 'Package not found or inactive'}), 404
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get reviews
        reviews = Review.query.filter_by(package_id=package_id).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        review_list = [review.to_dict() for review in reviews.items]
        
        # Calculate average rating
        all_reviews = Review.query.filter_by(package_id=package_id).all()
        if all_reviews:
            avg_rating = sum(review.rating for review in all_reviews) / len(all_reviews)
            total_reviews = len(all_reviews)
        else:
            avg_rating = 0
            total_reviews = 0
        
        return jsonify({
            'reviews': review_list,
            'average_rating': round(avg_rating, 1),
            'total_reviews': total_reviews,
            'total': reviews.total,
            'pages': reviews.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    try:
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        return jsonify({'review': review.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        # Check if user owns the review or is admin
        if review.user_id != user_id and user.role != UserRole.ADMIN:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'rating' in data:
            rating = data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
            review.rating = rating
        
        if 'comment' in data:
            review.comment = data['comment']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Review updated successfully',
            'review': review.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        review = Review.query.get(review_id)
        if not review:
            return jsonify({'error': 'Review not found'}), 404
        
        # Check if user owns the review or is admin
        if review.user_id != user_id and user.role != UserRole.ADMIN:
            return jsonify({'error': 'Access denied'}), 403
        
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({'message': 'Review deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user_reviews():
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Get user's reviews
        reviews = Review.query.filter_by(user_id=user_id).paginate(
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

@reviews_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_reviews():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Check if user is admin
        if user.role != UserRole.ADMIN:
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        package_filter = request.args.get('package_id', type=int)
        user_filter = request.args.get('user_id', type=int)
        
        # Build query
        query = Review.query
        
        if package_filter:
            query = query.filter_by(package_id=package_filter)
        
        if user_filter:
            query = query.filter_by(user_id=user_filter)
        
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
