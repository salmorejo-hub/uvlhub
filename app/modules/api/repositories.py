from app.modules.api.models import Api
from core.repositories.BaseRepository import BaseRepository


class ApiRepository(BaseRepository):
    def __init__(self):
        super().__init__(Api)
