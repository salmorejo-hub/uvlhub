from fakenodo.app.models import Deposition, Creator
from core.repositories.BaseRepository import BaseRepository


class DepositionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Deposition)


class CreatorRepository(BaseRepository):
    def __init__(self):
        super().__init(Creator)
