from app import db


class Discordbot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'Discordbot<{self.id}>'
