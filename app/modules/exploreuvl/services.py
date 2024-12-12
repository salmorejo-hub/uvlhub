from app.modules.exploreuvl.repositories import ExploreUVL
from core.services.BaseService import BaseService


class ExploreServiceUvl(BaseService):
    def __init__(self):
        super().__init__(ExploreUVL())

    def filter(self, query="", title="", description="", authors="", q_tags="", bytes="", publication_type="any", tags=[], **kwargs):
        return self.repository.filter(query, title, description, authors, q_tags, bytes, publication_type, tags, **kwargs)
