import hashlib
import logging
import random

from typing import List
from fakenodo.app.models import Deposition, File
from dotenv import load_dotenv
from core.services.BaseService import BaseService

logger = logging.getLogger(__name__)

load_dotenv()

# List where all depositions are stored
depositions: List[Deposition] = []
generated_ids = set()


class Service(BaseService):

    """
    ***Fakenodo is not connected to any database***

    There is no repositories in this module, we are using a simple list
    where all depositions are going to be stored.

    We dont consider to connect fakenodo to a database because this is not a real API,
    is only a test simulation API of Zenodo
    """

    def __init__(self):
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
                checksum=hashlib.md5(file_data).hexdigest(),
                deposition_id=deposition_id
            )

            target_deposition = self.get_deposition(deposition_id)
            if target_deposition is None:
                raise FileNotFoundError("Deposition not found")
            if target_deposition.files is None:
                target_deposition.files = [file_instance.to_dict()]
            else:
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
        if deposition.doi is not None:
            deposition.published = True
            
        return deposition.to_dict()

    def delete_deposition(self, deposition: Deposition) -> None:
        """Delete deposition

        Args:
            deposition(Deposition): deposition to be deleted
        """
        depositions.remove(deposition)

    def get_deposition(self, deposition_id: int) -> Deposition | None:
        """
        Get deposition by id.

        Args:
            deposition_id (int): ID of the target deposition.

        Returns:
            dict | None: The deposition with the given ID, or None if not found.
        """
        return [deposition for deposition in depositions if deposition_id == deposition.id][0]
    
    def generate_doi_id(self):
        while True:
            identifier = str(random.randint(10000, 99999))
            if identifier not in generated_ids:
                generated_ids.add(identifier)
                return identifier
            
    def generate_doi(self, deposition_id: int) -> None:
        """Generate doi to publish deposition
        Args:
            deposition_id(int): id of target deposition
        Returns:
            str: Doi of the target deposition
        """
        target_deposition = self.get_deposition(deposition_id)

        doi_id = self.generate_doi_id()

        target_deposition.doi = f"http://localhost/doi/{doi_id}/dataset.{doi_id}"
            
    def get_doi(self, deposition_id: int) -> str:
        """
        Get doi of a deposition, this function is only for api simulation purposes,

        Args:
            deposition_id(int): id of target deposition

        Returns:
            str: Doi of the target deposition
        """
        return self.get_deposition(deposition_id).doi
