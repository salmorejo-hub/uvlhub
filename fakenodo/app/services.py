import logging
import os
from typing import List
import requests

from app.modules.dataset.models import Author, DSMetaData, DataSet, PublicationType
from app.modules.featuremodel.models import FMMetaData, FMMetrics, FeatureModel
from app.modules.featuremodel.repositories import FeatureModelRepository
from app.modules.hubfile.models import Hubfile
from fakenodo.app.models import Deposition

from core.configuration.configuration import uploads_folder_name
from dotenv import load_dotenv
from flask import jsonify, Response
from flask_login import current_user



from core.services.BaseService import BaseService

logger = logging.getLogger(__name__)

load_dotenv()

depositions: List[Deposition] = []

author1 = Author(name="Jane Doe", affiliation="University of Example", orcid="0000-0001-2345-6789")
author2 = Author(name="Bob Jones", affiliation="Example Research Institute")
ds_meta_data = DSMetaData(
    deposition_id=123456,
    title="Sample DataSet for Testing",
    description="A comprehensive dataset for testing deposition creation.",
    publication_type=PublicationType.JOURNAL_ARTICLE,
    publication_doi="10.1000/journal.pone.1234567",
    dataset_doi="10.1000/dataset.abcdefg",
    tags="machine learning, data science, AI",
    authors=[author1, author2]
)
dataset = DataSet(
    id=1,
    user_id=101,
    ds_meta_data=ds_meta_data
)

metrics = FMMetrics(solver="Metric data for solver", not_solver="Metric data for not solver")

metadata = FMMetaData(
    uvl_filename="example.uvl",
    title="Sample Feature Model",
    description="This is a sample feature model metadata description.",
    publication_type=PublicationType.JOURNAL_ARTICLE,
    publication_doi="10.1234/example-doi",
    tags="sample, test, feature model",
    uvl_version="1.0",
    fm_metrics=metrics
)

feature_model = FeatureModel(data_set_id=1, fm_meta_data=metadata)



class FakenodoService(BaseService):
    
    def __init__(self):
        self.feature_model_repository = FeatureModelRepository()

    def get_fakenodo_url(self):

        FAKENODO_API_URL = os.getenv("FAKENODO_API_URL", "http://localhost:5001/api/fakenodo")
        print(f"Uri de fakenodo: ", FAKENODO_API_URL)
        
        return FAKENODO_API_URL

    
    def __init__(self):
        self.FAKENODO_API_URL = self.get_fakenodo_url()
        self.headers = {"Content-Type": "application/json"}

    def creation_test(self) -> bool:
        # Llamar a la función con el dataset creado
        response = self.create_new_deposition(dataset)
        print(f"Respuesta de la nueva creación: \n {response}")
        return response
        
    def test_full_connection(self) -> Response:
        """
        Test the connection with fakenodo by creating a deposition, uploading an empty test file, and deleting the
        deposition.

        Returns:
            bool: True if the connection, upload, and deletion are successful, False otherwise.
        """

        success = True

        # Create a test file
        working_dir = os.getenv('WORKING_DIR', "")
        file_path = os.path.join(working_dir, "test_file.txt")
        with open(file_path, "w") as f:
            f.write("This is a test file with some content.")

        messages = []  # List to store messages
        
        response = self.creation_test()
        print(f"Respuesta: \n {response}")
        
        if response['status_code'] != 201:
            return jsonify(
                {
                    "success": False,
                    "messages": f"Failed to create test deposition on fakenodo. Response code: {response['status_code']}",
                }
            )

        
        deposition_id = response['data']['id']

        data = {"name": "test_file.txt"}
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = self.upload_file(dataset,deposition_id,feature_model,file_path)
            # publish_url = f"{self.FAKENODO_API_URL}/deposition/{deposition_id}/files"
            # response = requests.post(publish_url, data=data, files=files)
        files["file"].close()  # Close the file after uploading
        print(f"Data: {data}")
        print(f"Files: {files}")
        print(f"Response Status Code: {response['status_code']}")
        print(f"Response Content: {response['data']}")

        if response["status_code"] != 201:
            messages.append(f"Failed to upload test file to fakenodo. Response code: {response['status_code']}")
            success = False

        #Step 3: Delete the deposition
        # for deposition in depositions:
        #     if deposition.to_dict()['id'] == deposition_id:
        #         depositions.remove(deposition)

        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({"success": success, "messages": messages})


    def get_all_depositions(self) -> dict:
        """
        Get all depositions from fakenodo.

        Returns:
            dict: The response in JSON format with the depositions.
        """
        
        deposition_list = [deposition.to_dict() for deposition in depositions]
        return deposition_list

    def create_new_deposition(self, dataset: DataSet) -> dict:
        """
        Create a new deposition in Fakenodo.

        Args:
            dataset (DataSet): The DataSet object containing the metadata of the deposition.

        Returns:
            dict: The response in JSON format with the details of the created deposition.
        """

        metadata = {
            "title": dataset.ds_meta_data.title,
            "upload_type": "dataset" if dataset.ds_meta_data.publication_type.value == "none" else "publication",
            "publication_type": (
                dataset.ds_meta_data.publication_type.value
                if dataset.ds_meta_data.publication_type.value != "none"
                else None
            ),
            "description": dataset.ds_meta_data.description,
            "creators": [
                {
                    "name": author.name,
                    **({"affiliation": author.affiliation} if author.affiliation else {}),
                    **({"orcid": author.orcid} if author.orcid else {}),
                }
                for author in dataset.ds_meta_data.authors
            ],
            "keywords": (
                ["uvlhub"] if not dataset.ds_meta_data.tags else dataset.ds_meta_data.tags.split(", ") + ["uvlhub"]
            ),
            "access_right": "open",
            "license": "CC-BY-4.0",
        }
        
        try:
            deposition = Deposition(**metadata)
            response_data = deposition.to_dict()
            depositions.append(deposition)
            return {'data': response_data, 'status_code': 201}
        except Exception as e:
                print(f"Error obtenido en la creación: {e}")
                return {'data': jsonify({"success": False, "message": str(e)}), 'status_code':500}



    def upload_file(self, dataset: DataSet, deposition_id: int, feature_model: FeatureModel,file_path, user=None) -> dict:
        """
        Upload a file to a deposition in Fakenodo.

        Args:
            deposition_id (int): The ID of the deposition in Fakenodo.
            feature_model (FeatureModel): The FeatureModel object representing the feature model.
            user (FeatureModel): The User object representing the file owner.

        Returns:
            dict: The response in JSON format with the details of the uploaded file.
        """
        uvl_filename = feature_model.fm_meta_data.uvl_filename
        data = {"name": uvl_filename}
        # user_id = current_user.id if user is None else user.id
        # file_path = os.path.join(uploads_folder_name(), f"user_{str(user_id)}", f"dataset_{dataset.id}/", uvl_filename)
        files = {"file": open(file_path, "rb")}
        
        try: 
            for file_obj in files.values():  # Usamos `values()` para obtener los objetos de archivo
                file_data = file_obj.read()
    
                file_instance = Hubfile(
                    name=data["name"],
                    size=len(file_data),
                    feature_model_id=feature_model.id)
        
                feature_model.files.append(file_instance)
                print(f"Resultados: {feature_model.files[0].to_dict()}")
            return {'data':jsonify(f'File uploaded succesfully: {data["name"]}'),'status_code':201}
        except Exception as e:
                print(f"Error en la subida del archivo: {e}")
                return {'data': jsonify(f"Failed to upload {data["name"]}, error_message: {e}"), 'status_code':500}


    def publish_deposition(self, deposition_id: int) -> dict:
        """
        Publish a deposition in Fakenodo.

        Args:
            deposition_id (int): The ID of the deposition in Fakenodo.

        Returns:
            dict: The response in JSON format with the details of the published deposition.
        """
        publish_url = f"{self.FA_API_URL}/{deposition_id}/actions/publish"
        response = requests.post(publish_url, params=self.params, headers=self.headers)
        if response.status_code != 202:
            raise Exception("Failed to publish deposition")
        return response.json()

    def get_deposition(self, deposition_id: int) -> Deposition:
        """
        Get a deposition from Fakenodo.

        Args:
            deposition_id (int): The ID of the deposition in Fakenodo.

        Returns:
            dict: The response in JSON format with the details of the deposition.
        """
        return [deposition.to_dict() for deposition in depositions if deposition.to_dict()['id'] == deposition_id][0]

    def get_doi(self, deposition_id: int) -> str:
        """
        Get the DOI of a deposition from Fakenodo.

        Args:
            deposition_id (int): The ID of the deposition in Fakenodo.

        Returns:
            str: The DOI of the deposition.
        """
        return self.get_deposition(deposition_id)['doi']
