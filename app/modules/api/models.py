from app import db


class APIToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'APIToken<{self.id}>'