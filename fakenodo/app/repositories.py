import app
from fakenodo.app.models import Fakenodo
from core.repositories.BaseRepository import BaseRepository

class FakenodoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Fakenodo)