from app.modules.api.repositories import ApiRepository
from core.services.BaseService import BaseService


class ApiService(BaseService):
    def __init__(self):
        super().__init__(ApiRepository())
