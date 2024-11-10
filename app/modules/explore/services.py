from app.modules.explore.repositories import ExploreRepository
from core.services.BaseService import BaseService


class ExploreService(BaseService):
    def __init__(self):
        super().__init__(ExploreRepository())

    def filter(self, query="", sorting="newest", publication_type="any", tags=[], min_number_of_models=0, 
               max_number_of_models=100, min_number_of_features=0, max_number_of_features=100, **kwargs):
        return self.repository.filter(query, sorting, publication_type, tags, min_number_of_models, 
                                      max_number_of_models, min_number_of_features, max_number_of_features, **kwargs)
