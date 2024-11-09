from app import db
from datetime import datetime


class APIToken(db.Model):
    __tablename__ = 'api_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship("User", backref="api_tokens")

    def is_expired(self):
        return datetime.datetime.now(datetime.timezone.utc) > self.expiration_date

    def __repr__(self):
        return f'APIToken<{self.id}>'
