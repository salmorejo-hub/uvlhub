import requests
from app.modules.dataset.tests.test_selenium import test_upload_dataset

FAKENODO_API_URL = 'http://localhost:5001/api/fakenodo/depositions'


def test_upload_dataset_to_fakenodo():
    test_upload_dataset()

    response = requests.get(FAKENODO_API_URL)
    assert response.status_code == 200, "API request failed"
    datasets = response.json()

    assert len(datasets) == 3, "Some dataset failed to upload"

    for i, dataset in enumerate(datasets, start=1):
        assert dataset["access_right"] == "open", f"Dataset {i} has incorrect access_right"
        assert dataset["title"] == "Title", f"Dataset {i} has incorrect title"
        assert dataset["description"] == "Description", f"Dataset {i} has incorrect description"
        assert dataset["license"] == "CC-BY-4.0", f"Dataset {i} has incorrect license"
        assert dataset["upload_type"] == "dataset", f"Dataset {i} has incorrect upload_type"
        assert dataset["published"] is True, f"Dataset {i} is not published"
        assert len(dataset["creators"]) == 3, f"Dataset {i} has incorrect number of creators"

        assert len(dataset["files"]) == 2, f"Dataset {i} has incorrect number of files"
        expected_files = [
            {"checksum": "01939e8e60a452b828b60db125a1758c", "size": 1024},
            {"checksum": "67a574babd23cbaefc70f4fce14e5b07", "size": 2048}
        ]
        for j, file in enumerate(dataset["files"], start=1):
            expected_file = expected_files[j - 1]
            assert file["size"] == expected_file["size"], f"File {j} in dataset {i} has incorrect size"
            assert file["checksum"] == expected_file["checksum"], f"File {j} in dataset {i} has incorrect checksum"
