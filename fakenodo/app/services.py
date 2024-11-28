import hashlib
import logging

from typing import List
from app.modules.featuremodel.repositories import FeatureModelRepository
from fakenodo.app.models import Deposition, File
from dotenv import load_dotenv
from core.services.BaseService import BaseService

logger = logging.getLogger(__name__)

load_dotenv()

# List where all depositions are stored
depositions: List[Deposition] = []


class Service(BaseService):

    """
    ***Fakenodo is not connected to any database***

    There is no repositories in this module, we are using a simple list
    where all depositions are going to be stored.

    We dont consider to connect fakenodo to a database because this is not a real API,
    is only a test simulation API of Zenodo
    """

    def __init__(self):
        self.feature_model_repository = FeatureModelRepository()
        self.headers = {"Content-Type": "application/json"}

    def get_all_depositions(self) -> list:
        """
        Get all depositions from fakenodo.

        Returns:
            dict: dict of all fakenodo depositions
        """
        return [deposition.to_dict() for deposition in depositions]

    def create_new_deposition(self, deposition: Deposition) -> dict:
        """Create new deposition

        Args:
            deposition(Deposition): new deposition

        Returns:
            dict: dict of the new deposition
        """
        depositions.append(deposition)
        return deposition.to_dict()

    def upload_file(self, file, deposition_id) -> None:
        """Upload file into fakenodo deposition

        Args:
            file(File): uvl file give in create dataset form
            deposition_id(int): id of the target deposition where the file is going to be uploaded
        """

        try:
            # Read file content
            file_data = file.read()

            # Create the file instance
            file_instance = File(
                name=file.filename,
                size=len(file_data),
                checksum=hashlib.md5(file_data).hexdigest()
            )
            target_deposition = self.get_deposition(deposition_id)
            target_deposition.files.append(file_instance.to_dict())

        except Exception as e:
            print(f"Error en la subida del archivo: {e}")

    def publish_deposition(self, deposition: Deposition) -> dict:
        """Publish deposition, this function is only for api simulation purposes,
        fakenodo doesn't synchronize depositions with uvlhub

        Args:
            deposition(Deposition): deposition to be published
        Returns:
            dict: published deposition
        """

        deposition.published = True
        return deposition.to_dict()

    def delete_deposition(self, deposition: Deposition) -> None:
        """Delete deposition

        Args:
            deposition(Deposition): deposition to be deleted
        """
        depositions.remove(deposition)

    def get_deposition(self, deposition_id: int) -> dict:
        """Get deposition by id

        Args:
            deposition_id(int): id of the target deposition
        Returns:
            dict: deposition with id given as parameter
        """
        return [deposition for deposition in depositions if deposition.to_dict()['id'] == deposition_id][0]

    def get_doi(self, deposition_id: int) -> str:
        """
        Get doi of a deposition, this function is only for api simulation purposes,
        fakenodo doesn´t generate doi.

        Args:
            deposition_id(int): id of target deposition

        Returns:
            str: Doi of the target deposition
        """
        return self.get_deposition(deposition_id)['doi']
