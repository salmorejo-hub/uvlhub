from app.modules.discordbot.repositories import DiscordbotRepository
from core.services.BaseService import BaseService


class DiscordbotService(BaseService):
    def __init__(self):
        super().__init__(DiscordbotRepository())
