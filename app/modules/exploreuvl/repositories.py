import re
from sqlalchemy import any_, and_, or_
import unidecode
from app.modules.dataset.models import Author, PublicationType
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository


class ExploreUVL(BaseRepository):
    def __init__(self):
        super().__init__(FeatureModel)

    def filter(self, query="", q_title="", q_description="", q_authors="", q_tags="", q_bytes="", publication_type="any", tags=[], **kwargs):
        
        if query=="":
            filters = {'title': q_title, 'description': q_description, 'authors': q_authors, 'tags': q_tags} 
            q_filters = []
            author_filters = []
            for type in filters:
                normalized_query = unidecode.unidecode(filters[type]).lower()
                cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)
                if type == 'title' and not filters[type]=="":
                    q_filters.append(FMMetaData.title.ilike(f"%{cleaned_query}%"))
                if type == 'description' and not filters[type]=="":
                    q_filters.append(FMMetaData.description.ilike(f"%{cleaned_query}%"))
                if type == 'authors' and not filters[type]=="":
                    author_filters.append(Author.name.ilike(f"%{cleaned_query}%"))
                    author_filters.append(Author.affiliation.ilike(f"%{cleaned_query}%"))
                    author_filters.append(Author.orcid.ilike(f"%{cleaned_query}%"))
                if type == 'tags' and not filters[type]=="":
                    q_filters.extend([FMMetaData.tags.ilike(f"%{q}%") for q in cleaned_query.split()])

            uvls = (
                self.model.query
                .join(FeatureModel.fm_meta_data)
                .join(FMMetaData.authors)
                .filter(or_(*author_filters))
                .filter(and_(*q_filters))
                .filter(FMMetaData.publication_doi.isnot(None))
            )
            
        else:
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

        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                uvls = uvls.filter(FMMetaData.publication_type == matching_type.name)

        if tags:
            uvls = uvls.filter(FMMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))
  
        if isinstance(q_bytes, int):
            return list(filter(lambda uvl: uvl.get_total_files_size() <= q_bytes, uvls.all()))
                
        return uvls.all()
