from app.modules.rating.models import Rating
from core.repositories.BaseRepository import BaseRepository

class RatingRepository(BaseRepository):
    def __init__(self):
        super().__init__(Rating)

    def get_average_rating(self, dataset_id):
        ratings = self.model.query.filter_by(dataset_id=dataset_id).all()
        if not ratings:
            return 0
        return sum(rating.rating for rating in ratings) / len(ratings)

    def add_or_update_rating(self, user_id, dataset_id, rating_value):
        existing_rating = self.model.query.filter_by(user_id=user_id, dataset_id=dataset_id).first()
        if existing_rating:
            existing_rating.rating = rating_value
        else:
            new_rating = Rating(user_id=user_id, dataset_id=dataset_id, rating=rating_value)
            self.session.add(new_rating)
        self.session.commit()

    def get_user_rating(self, user_id, dataset_id):
        rating = self.model.query.filter_by(user_id=user_id, dataset_id=dataset_id).first()
        return rating.rating if rating else None
