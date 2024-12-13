from app.modules.rating.repositories import RatingRepository


class RatingService:
    def __init__(self):
        self.rating_repository = RatingRepository()

    def add_or_update_rating(self, user_id, dataset_id, rating_value):
        return self.rating_repository.add_or_update_rating(user_id, dataset_id, rating_value)

    def get_average_rating(self, dataset_id):
        return self.rating_repository.get_average_rating(dataset_id)

    def get_user_rating(self, user_id, dataset_id):
        return self.rating_repository.get_user_rating(user_id, dataset_id)
