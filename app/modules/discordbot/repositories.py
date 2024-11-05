from app.modules.discordbot.models import Discordbot
from core.repositories.BaseRepository import BaseRepository


class DiscordbotRepository(BaseRepository):
    def __init__(self):
        super().__init__(Discordbot)
