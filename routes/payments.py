from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Payment, Booking, User, UserRole, PaymentStatus
import razorpay
import os
import json

payments_bp = Blueprint('payments', __name__)

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET'))
)

@payments_bp.route('/create-order', methods=['POST'])
@jwt_required()
def create_payment_order():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'booking_id' not in data:
            return jsonify({'error': 'booking_id is required'}), 400
        
        booking = Booking.query.get(data['booking_id'])
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if user owns the booking
        if booking.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Check if booking is in pending status
        if booking.status.value != 'pending':
            return jsonify({'error': 'Booking is not in pending status'}), 400
        
        # Check if payment already exists
        existing_payment = Payment.query.filter_by(booking_id=booking.id).first()
        if existing_payment and existing_payment.status == PaymentStatus.COMPLETED:
            return jsonify({'error': 'Payment already completed for this booking'}), 400
        
        # Create Razorpay order
        order_data = {
            'amount': int(booking.total_amount * 100),  # Convert to paise
            'currency': 'INR',
            'receipt': f'booking_{booking.id}',
            'notes': {
                'booking_id': booking.id,
                'user_id': user_id,
                'package_title': booking.package.title
            }
        }
        
        razorpay_order = razorpay_client.order.create(data=order_data)
        
        # Create or update payment record
        if existing_payment:
            existing_payment.razorpay_order_id = razorpay_order['id']
            existing_payment.amount = booking.total_amount
            existing_payment.status = PaymentStatus.PENDING
            payment = existing_payment
        else:
            payment = Payment(
                booking_id=booking.id,
                razorpay_order_id=razorpay_order['id'],
                amount=booking.total_amount,
                currency='INR',
                status=PaymentStatus.PENDING
            )
            db.session.add(payment)
        
        db.session.commit()
        
        return jsonify({
            'order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency'],
            'payment_id': payment.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/verify', methods=['POST'])
@jwt_required()
def verify_payment():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['razorpay_payment_id', 'razorpay_order_id', 'razorpay_signature']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': data['razorpay_order_id'],
            'razorpay_payment_id': data['razorpay_payment_id'],
            'razorpay_signature': data['razorpay_signature']
        }
        
        try:
            razorpay_client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            return jsonify({'error': 'Payment verification failed'}), 400
        
        # Find payment record
        payment = Payment.query.filter_by(
            razorpay_order_id=data['razorpay_order_id']
        ).first()
        
        if not payment:
            return jsonify({'error': 'Payment record not found'}), 404
        
        # Check if user owns the payment
        if payment.booking.user_id != user_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Update payment status
        payment.razorpay_payment_id = data['razorpay_payment_id']
        payment.status = PaymentStatus.COMPLETED
        payment.payment_method = 'razorpay'
        
        # Update booking status
        payment.booking.status = 'confirmed'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payment verified successfully',
            'payment': payment.to_dict(),
            'booking': payment.booking.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/status/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_payment_status(payment_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        payment = Payment.query.get(payment_id)
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        # Check if user owns the payment or is admin
        if payment.booking.user_id != user_id and user.role != UserRole.ADMIN:
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({'payment': payment.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/booking/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking_payments(booking_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Check if user owns the booking or is admin
        if booking.user_id != user_id and user.role != UserRole.ADMIN:
            return jsonify({'error': 'Access denied'}), 403
        
        payments = Payment.query.filter_by(booking_id=booking_id).all()
        payment_list = [payment.to_dict() for payment in payments]
        
        return jsonify({'payments': payment_list}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/refund', methods=['POST'])
@jwt_required()
def create_refund():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Check if user is admin
        if user.role != UserRole.ADMIN:
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        if 'payment_id' not in data:
            return jsonify({'error': 'payment_id is required'}), 400
        
        payment = Payment.query.get(data['payment_id'])
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404
        
        if payment.status != PaymentStatus.COMPLETED:
            return jsonify({'error': 'Payment is not completed'}), 400
        
        # Create Razorpay refund
        refund_data = {
            'payment_id': payment.razorpay_payment_id,
            'amount': int(payment.amount * 100),  # Convert to paise
            'notes': {
                'reason': data.get('reason', 'Refund requested by admin'),
                'booking_id': payment.booking_id
            }
        }
        
        try:
            razorpay_refund = razorpay_client.payment.refund(
                payment.razorpay_payment_id, refund_data
            )
        except Exception as e:
            return jsonify({'error': f'Refund failed: {str(e)}'}), 500
        
        # Update payment status
        payment.status = PaymentStatus.REFUNDED
        
        # Update booking status
        payment.booking.status = 'cancelled'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Refund processed successfully',
            'refund_id': razorpay_refund['id'],
            'payment': payment.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_payments():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Check if user is admin
        if user.role != UserRole.ADMIN:
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        booking_id = request.args.get('booking_id', type=int)
        
        # Build query
        query = Payment.query
        
        if status:
            try:
                status_enum = PaymentStatus(status)
                query = query.filter_by(status=status_enum)
            except ValueError:
                return jsonify({'error': 'Invalid status'}), 400
        
        if booking_id:
            query = query.filter_by(booking_id=booking_id)
        
        # Paginate results
        payments = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        payment_list = [payment.to_dict() for payment in payments.items]
        
        return jsonify({
            'payments': payment_list,
            'total': payments.total,
            'pages': payments.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
