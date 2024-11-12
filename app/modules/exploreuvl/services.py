from app.modules.exploreuvl.repositories import ExploreUVL
from core.services.BaseService import BaseService


class ExploreServiceUvl(BaseService):
    def __init__(self):
        super().__init__(ExploreUVL())

    def filter(self, query="", publication_type="any", tags=[], **kwargs):
        return self.repository.filter(query, publication_type, tags, **kwargs)
    

