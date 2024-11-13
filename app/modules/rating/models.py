from datetime import datetime
from app import db
from flask_login import UserMixin

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dataset_id = db.Column(db.Integer, db.ForeignKey('data_set.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    dataset = db.relationship('DataSet', backref=db.backref('ratings', lazy=True))

    def __repr__(self):
        return f'<Rating user_id={self.user_id} dataset_id={self.dataset_id} rating={self.rating}>'
