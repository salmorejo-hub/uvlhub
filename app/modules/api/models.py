from app import db


class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'Api<{self.id}>'
