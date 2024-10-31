import logging
import os
import requests

from app.modules.dataset.models import DataSet
from app.modules.featuremodel.models import FeatureModel
from fakenodo.app.models import Deposition
from fakenodo.app.repositories import FakenodoRepository

from core.configuration.configuration import uploads_folder_name
from dotenv import load_dotenv
from flask import jsonify, Response
from flask_login import current_user



from core.services.BaseService import BaseService

logger = logging.getLogger(__name__)

load_dotenv()


class FakenodoService(BaseService):

    def get_fakenodo_url(self):

        FAKENODO_API_URL = os.getenv("FAKENODO_API_URL", "http://localhost:5001/api/fakenodo")
        print(f"Uri de fakenodo: ", FAKENODO_API_URL)
        
        return FAKENODO_API_URL

    '''def get_Fakenodo_access_token(self):
        return os.getenv("ZENODO_ACCESS_TOKEN")
    '''
    
    def __init__(self):
        super().__init__(FakenodoRepository())
        #self.ZENODO_ACCESS_TOKEN = self.get_zenodo_access_token()
        self.FAKENODO_API_URL = self.get_fakenodo_url()
        self.headers = {"Content-Type": "application/json"}
        #self.params = {"access_token": self.ZENODO_ACCESS_TOKEN}

    def test_connection(self) -> bool:
        """
        Test the connection with fakenodo.

        Returns:
            bool: True if the connection is successful, False otherwise.
        """
        response = requests.get(self.FAKENODO_API_URL, headers=self.headers)
        return response.status_code == 200

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

        # Step 1: Create a deposition on fakenodo
        data = {
            "metadata": {
                "id":1,
                "title": "Test Deposition",
                "upload_type": "dataset",
                "description": "This is a test deposition created via fakenodo API",
                "creators": [{"name": "John Doe"}],
            }
        }

        response = requests.post(f"{self.FAKENODO_API_URL}/deposition/empty", json=data, headers=self.headers)
        


        if response.status_code != 201:
            return jsonify(
                {
                    "success": False,
                    "messages": f"Failed to create test deposition on fakenodo. Response code: {response.status_code}",
                }
            )

        
        deposition_id = 1

        data = {"name": "test_file.txt"}
        with open(file_path, "rb") as f:
            files = {"file": f}
            publish_url = f"{self.FAKENODO_API_URL}/deposition/{deposition_id}/files"
            response = requests.post(publish_url, data=data, files=files)
        files["file"].close()  # Close the file after uploading


        print(f"Publish URL: {publish_url}")
        print(f"Data: {data}")
        print(f"Files: {files}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response._content}")

        if response.status_code != 201:
            messages.append(f"Failed to upload test file to fakenodo. Response code: {response.status_code}")
            success = False

        # Step 3: Delete the deposition
        response = requests.delete(f"{self.FAKENODO_API_URL}/{deposition_id}")

        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({"success": success, "messages": messages})

    def get_all_depositions(self) -> dict:
        """
        Get all depositions from fakenodo.

        Returns:
            dict: The response in JSON format with the depositions.
        """
        response = requests.get("f{self.FAKENODO_API_URL}/depositions", headers=self.headers)
        if response.status_code != 200:
            raise Exception("Failed to get depositions")
        return response.json()

    def create_new_deposition(self, dataset: DataSet) -> dict:
        """
        Create a new deposition in Fakenodo.

        Args:
            dataset (DataSet): The DataSet object containing the metadata of the deposition.

        Returns:
            dict: The response in JSON format with the details of the created deposition.
        """

        logger.info("Dataset sending to Fakenodo...")
        logger.info(f"Publication type...{dataset.ds_meta_data.publication_type.value}")

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

        data = {"metadata": metadata}

        response = requests.post(self.FAKENODO_API_URL, params=self.params, json=data, headers=self.headers)
        if response.status_code != 201:
            error_message = f"Failed to create deposition. Error details: {response.json()}"
            raise Exception(error_message)
        return response.json()

    def upload_file(self, dataset: DataSet, deposition_id: int, feature_model: FeatureModel, user=None) -> dict:
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
        user_id = current_user.id if user is None else user.id
        file_path = os.path.join(uploads_folder_name(), f"user_{str(user_id)}", f"dataset_{dataset.id}/", uvl_filename)
        files = {"file": open(file_path, "rb")}

        publish_url = f"{self.FAKENODO_API_URL}/{deposition_id}/files"
        response = requests.post(publish_url, params=self.params, data=data, files=files)
        if response.status_code != 201:
            error_message = f"Failed to upload files. Error details: {response.json()}"
            raise Exception(error_message)
        return response.json()

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

    def get_deposition(self, deposition_id: int) -> dict:
        """
        Get a deposition from Fakenodo.

        Args:
            deposition_id (int): The ID of the deposition in Fakenodo.

        Returns:
            dict: The response in JSON format with the details of the deposition.
        """
        deposition_url = f"{self.FAKENODO_API_URL}/{deposition_id}"
        response = requests.get(deposition_url, params=self.params, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Failed to get deposition")
        return response.json()

    def get_doi(self, deposition_id: int) -> str:
        """
        Get the DOI of a deposition from Fakenodo.

        Args:
            deposition_id (int): The ID of the deposition in Fakenodo.

        Returns:
            str: The DOI of the deposition.
        """
        return self.get_deposition(deposition_id).get("doi")
