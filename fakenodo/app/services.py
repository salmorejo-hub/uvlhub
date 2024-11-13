import hashlib
import logging
import os
from typing import List
import requests

from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FMMetaData, FMMetrics, FeatureModel
from app.modules.featuremodel.repositories import FeatureModelRepository
from app.modules.hubfile.models import Hubfile
from fakenodo.app.models import Deposition, File

from core.configuration.configuration import uploads_folder_name
from dotenv import load_dotenv
from flask import jsonify, Response
from flask_login import current_user



from core.services.BaseService import BaseService

logger = logging.getLogger(__name__)

load_dotenv()

depositions: List[Deposition] = []

class Service(BaseService):

    def __init__(self):
        self.feature_model_repository = FeatureModelRepository()

    # def get_fakenodo_url(self):

    #     FAKENODO_API_URL = os.getenv("FAKENODO_API_URL", "http://localhost:5001/api/fakenodo")
        
    #     return FAKENODO_API_URL

    
    def __init__(self):
        #self.FAKENODO_API_URL = self.get_fakenodo_url()
        self.headers = {"Content-Type": "application/json"}


    def get_all_depositions(self) -> list:
        """
        Get all depositions from fakenodo.

        Returns:
            dict: The response in JSON format with the depositions.
        """
        
        return [deposition.to_dict() for deposition in depositions]


    def create_new_deposition(self, deposition: Deposition) -> dict:
        response_data = deposition.to_dict()
        depositions.append(deposition)
        return response_data


    def upload_file(self,file,data,deposition_id) -> None:
        try: 
    
            file_data = file.read()
            print(f'Datos: {data},{file},{file_data}')
            
            file_instance =File(
                name = file.filename,
                size=len(file_data),
                checksum= hashlib.md5(file_data).hexdigest()
            )
            target_deposition = self.get_deposition(deposition_id)
            target_deposition.files.clear()
            target_deposition.files.append(file_instance.to_dict())
                
        except Exception as e:
                print(f"Error en la subida del archivo: {e}")

    def publish_deposition(self, deposition:Deposition) -> None:
        deposition.published = True
        
        return deposition
    
    def delete_deposition(self, deposition:Deposition) -> None:
        depositions.remove(deposition)
        

    
    def get_deposition(self, deposition_id: int) -> dict:
        return [deposition for deposition in depositions if deposition.to_dict()['id'] == deposition_id][0]

    def get_doi(self, deposition_id: int) -> str:
        return self.get_deposition(deposition_id)['doi']
