import re
from sqlalchemy import or_
import unidecode
from app.modules.dataset.models import Author
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository


class ExploreUVL(BaseRepository):
    def __init__(self):
        super().__init__(FeatureModel)

    def filter(self, query="", publication_type="any",  tags=[], **kwargs):
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        filters = []
        for word in cleaned_query.split():
            filters.append(FMMetaData.title.ilike(f"%{word}%"))
            filters.append(FMMetaData.description.ilike(f"%{word}%"))
            filters.append(Author.name.ilike(f"%{word}%"))
            filters.append(Author.affiliation.ilike(f"%{word}%"))
            filters.append(Author.orcid.ilike(f"%{word}%"))
            filters.append(FMMetaData.uvl_filename.ilike(f"%{word}%"))
            filters.append(FMMetaData.tags.ilike(f"%{word}%"))

        uvls = (
            self.model.query
            .join(FeatureModel.fm_meta_data)
            .join(FMMetaData.authors)
            .filter(or_(*filters))
            .filter(FMMetaData.publication_doi.isnot(None))
        )

        if tags:
            for tag in tags:
                uvls = uvls.filter(FMMetaData.tags.ilike(f"%{tag}%"))
        return uvls.all()
