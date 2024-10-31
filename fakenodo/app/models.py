
import app

class Fakenodo(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)

from app import db

class Creator(db.Model):
    __tablename__ = 'creators'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    deposition_id = db.Column(db.Integer, db.ForeignKey('depositions.id'), nullable=False)
    
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'name': self.name
        }

class Deposition(db.Model):
    __tablename__ = 'depositions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    upload_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    creators = db.relationship('Creator', backref='deposition', lazy=True, cascade="all, delete")

    def __init__(self, metadata):
        self.title = metadata.get('title')
        self.upload_type = metadata.get('upload_type')
        self.description = metadata.get('description')
        
        # Inicializa los creadores a partir del JSON en metadata
        creator_data = metadata.get('creators', [])
        self.creators = [Creator(**creator) for creator in creator_data]

    def to_dict(self):
        return {
                'id': self.id,
                'title': self.title,
                'upload_type': self.upload_type,
                'description': self.description,
                'creators': [creator.to_dict() for creator in self.creators]
            }
    

    def __repr__(self):
        return f"<Deposition(title={self.title}, upload_type={self.upload_type})>"
