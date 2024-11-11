from app.modules.api.models import APIToken
from core.repositories.BaseRepository import BaseRepository


class APIRepository(BaseRepository):
    def __init__(self):
        super().__init__(APIToken)
