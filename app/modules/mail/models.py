from app import db


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'Mail<{self.id}>'
