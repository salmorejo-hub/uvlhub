from app.modules.explore.repositories import ExploreRepository
from core.services.BaseService import BaseService


class ExploreService(BaseService):
    def __init__(self):
        super().__init__(ExploreRepository())

    def filter(self, query="", sorting="newest", publication_type="any", tags=[], min_number_of_models=None, max_number_of_models=None,
               min_number_of_features=None, max_number_of_features=None,**kwargs):
        return self.repository.filter(query, sorting, publication_type, tags, min_number_of_models, max_number_of_models, 
                                      min_number_of_features, max_number_of_features, **kwargs)
