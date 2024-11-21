from flask_restful import Resource
from flask import request, jsonify
from flask_login import login_required, current_user
from app.modules.rating.services import RatingService

rating_service = RatingService()

class RatingResource(Resource):
   
    @login_required
    def post(self, dataset_id):
        data = request.get_json()
        rating_value = data.get('rating')

        if not rating_value or not (1 <= rating_value <= 5):
            return jsonify({"message": "Rating must be between 1 and 5."}), 400

        try:
            rating_service.add_or_update_rating(current_user.id, dataset_id, rating_value)
            return jsonify({"message": "Rating submitted successfully."}), 200
        except Exception as e:
            return jsonify({"message": "Error submitting rating.", "error": str(e)}), 500

    def get(self, dataset_id):
        try:
            average_rating = rating_service.get_average_rating(dataset_id)
            if average_rating is None:
                return jsonify({"message": "No ratings available for this dataset."}), 404
            return jsonify({"average_rating": average_rating}), 200
        except Exception as e:
            return jsonify({"message": "Error fetching rating.", "error": str(e)}), 500


def init_blueprint_api(api):
    api.add_resource(RatingResource, '/api/v1/rating/<int:dataset_id>', endpoint='rating')
