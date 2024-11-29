import re
from sqlalchemy import any_, or_, cast, Integer, func
import unidecode
from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType, DSMetrics
from app.modules.featuremodel.models import FMMetaData, FeatureModel
from core.repositories.BaseRepository import BaseRepository


class ExploreRepository(BaseRepository):
    def __init__(self):
        super().__init__(DataSet)

    def filter(self, query="", sorting="newest", publication_type="any", tags=[], min_number_of_models=0,
               max_number_of_models=100, min_number_of_features=0, max_number_of_features=100, day="", month="",
               year="", max_size=None, size_unit="bytes", **kwargs):
        # Normalize and remove unwanted characters
        normalized_query = unidecode.unidecode(query).lower()
        cleaned_query = re.sub(r'[,.":\'()\[\]^;!¡¿?]', "", normalized_query)

        filters = []
        for word in cleaned_query.split():
            filters.append(DSMetaData.title.ilike(f"%{word}%"))
            filters.append(DSMetaData.description.ilike(f"%{word}%"))
            filters.append(Author.name.ilike(f"%{word}%"))
            filters.append(Author.affiliation.ilike(f"%{word}%"))
            filters.append(Author.orcid.ilike(f"%{word}%"))
            filters.append(FMMetaData.uvl_filename.ilike(f"%{word}%"))
            filters.append(FMMetaData.title.ilike(f"%{word}%"))
            filters.append(FMMetaData.description.ilike(f"%{word}%"))
            filters.append(FMMetaData.publication_doi.ilike(f"%{word}%"))
            filters.append(FMMetaData.tags.ilike(f"%{word}%"))
            filters.append(DSMetaData.tags.ilike(f"%{word}%"))

        datasets = (
            self.model.query
            .join(DataSet.ds_meta_data)
            .join(DSMetaData.authors)
            .join(DataSet.feature_models)
            .join(FeatureModel.fm_meta_data)
            .filter(or_(*filters))
            .filter(DSMetaData.dataset_doi.isnot(None))  # Exclude datasets with empty dataset_doi
        )

        if publication_type != "any":
            matching_type = None
            for member in PublicationType:
                if member.value.lower() == publication_type:
                    matching_type = member
                    break

            if matching_type is not None:
                datasets = datasets.filter(DSMetaData.publication_type == matching_type.name)

        if tags:
            datasets = datasets.filter(DSMetaData.tags.ilike(any_(f"%{tag}%" for tag in tags)))

        if day != "":
            datasets = datasets.filter(func.extract('day', DataSet.created_at) == int(day))

        if month != "":
            datasets = datasets.filter(func.extract('month', DataSet.created_at) == int(month))

        if year != "":
            datasets = datasets.filter(func.extract('year', DataSet.created_at) == int(year))

        # Order by created_at
        if sorting == "oldest":
            datasets = datasets.order_by(self.model.created_at.asc())
        else:
            datasets = datasets.order_by(self.model.created_at.desc())

        # Filter by number of models and features
        datasets = datasets.filter(
            DSMetaData.ds_metrics.has(
                (cast(DSMetrics.number_of_models, Integer) >= min_number_of_models) &
                (cast(DSMetrics.number_of_models, Integer) <= max_number_of_models) &
                (cast(DSMetrics.number_of_features, Integer) >= min_number_of_features) &
                (cast(DSMetrics.number_of_features, Integer) <= max_number_of_features)
            )
        ).all()

        # This filter operates on the datasets list that was returned by the previous filters that used ORM queries.
        if max_size is not None:
            if size_unit == "kb":
                max_size_bytes = max_size * 1024
            elif size_unit == "mb":
                max_size_bytes = max_size * 1024 ** 2
            elif size_unit == "gb":
                max_size_bytes = max_size * 1024 ** 3
            else:
                max_size_bytes = max_size
            datasets = [dataset for dataset in datasets if dataset.get_file_total_size() <= max_size_bytes]

        return datasets
