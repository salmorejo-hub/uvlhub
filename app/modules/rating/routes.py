from flask import jsonify, request
from flask_login import login_required, current_user
from app.modules.rating.services import RatingService
from app.modules.rating import rating_bp

rating_service = RatingService()


@rating_bp.route('/dataset/<int:dataset_id>/rating', methods=['POST'])
@login_required
def rate_dataset(dataset_id):
    rating_value = request.json.get('rating')

    if not rating_value or not (1 <= rating_value <= 5):
        return jsonify({'message': 'Rating must be between 1 and 5.'}), 400

    rating_service.add_or_update_rating(current_user.id, dataset_id, rating_value)
    return jsonify({'message': 'Rating submitted successfully.'}), 200


@rating_bp.route('/dataset/<int:dataset_id>/rating', methods=['GET'])
def get_rating(dataset_id):
    average_rating = rating_service.get_average_rating(dataset_id)
    if average_rating is None:
        return jsonify({'message': 'No ratings available for this dataset.'}), 404
    return jsonify({'average_rating': average_rating}), 200


@rating_bp.route('/dataset/<int:dataset_id>/user-rating', methods=['GET'])
@login_required
def get_user_rating(dataset_id):
    user_rating = rating_service.get_user_rating(current_user.id, dataset_id)
    if user_rating is None:
        return jsonify({'message': 'No rating found for this user.'}), 404
    return jsonify({'user_rating': user_rating}), 200
