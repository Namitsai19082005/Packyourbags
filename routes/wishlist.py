from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, TravelPackage, Wishlist
from datetime import datetime

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/', methods=['GET'])
@jwt_required()
def get_wishlist():
    try:
        user_id = get_jwt_identity()
        
        # Get user's wishlist
        wishlist_items = db.session.query(Wishlist, TravelPackage).join(
            TravelPackage, Wishlist.package_id == TravelPackage.id
        ).filter(
            Wishlist.user_id == user_id,
            TravelPackage.is_active == True
        ).all()
        
        wishlist = []
        for wishlist_item, package in wishlist_items:
            package_dict = package.to_dict()
            wishlist.append({
                'id': wishlist_item.id,
                'package': package_dict,
                'added_at': wishlist_item.added_at.isoformat()
            })
        
        return jsonify({
            'success': True,
            'wishlist': wishlist
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@wishlist_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'package_id' not in data:
            return jsonify({'error': 'Package ID is required'}), 400
        
        package_id = data['package_id']
        
        # Check if package exists and is active
        package = TravelPackage.query.get(package_id)
        if not package or not package.is_active:
            return jsonify({'error': 'Package not found'}), 404
        
        # Check if already in wishlist
        existing = Wishlist.query.filter_by(
            user_id=user_id, 
            package_id=package_id
        ).first()
        
        if existing:
            return jsonify({'error': 'Package already in wishlist'}), 400
        
        # Add to wishlist
        wishlist_item = Wishlist(
            user_id=user_id,
            package_id=package_id
        )
        
        db.session.add(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Added to wishlist successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@wishlist_bp.route('/<int:package_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(package_id):
    try:
        user_id = get_jwt_identity()
        
        # Find wishlist item
        wishlist_item = Wishlist.query.filter_by(
            user_id=user_id,
            package_id=package_id
        ).first()
        
        if not wishlist_item:
            return jsonify({'error': 'Package not in wishlist'}), 404
        
        # Remove from wishlist
        db.session.delete(wishlist_item)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Removed from wishlist successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
