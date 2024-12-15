import pytest
from unittest.mock import patch
from flask import url_for
from app import create_app
import os


@pytest.fixture(scope='module')
def test_client():
    os.environ['FLASK_ENV'] = 'testing'

    # Crear la aplicación
    app = create_app()
    app.config['SERVER_NAME'] = 'localhost'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    with app.app_context():
        with app.test_client() as client:
            yield client

# Mock services


@pytest.fixture(scope="function")
def mock_dataset_service():
    with patch('app.modules.dataset.services.DataSetService') as mock:
        yield mock


@pytest.fixture(scope="function")
def mock_zenodo_service():
    with patch('app.modules.zenodo.services.ZenodoService') as mock:
        yield mock


def test_download_all_datasets(test_client, mock_dataset_service):
    mock_service_instance = mock_dataset_service.return_value
    mock_service_instance.zip_datasets.return_value = None

    # Mock para la función send_file que simula el envío del archivo
    with patch('app.modules.dataset.routes.send_file') as mock_send_file:
        mock_send_file.return_value = "Zip sent"

        response = test_client.get(url_for('dataset.download_all_datasets'))
        assert response.status_code == 200, response.status_code
        assert response.data == b"Zip sent", response.data


def test_download_all_datasets_empty_directory(test_client, mock_dataset_service):
    mock_service_instance = mock_dataset_service.return_value
    mock_service_instance.zip_datasets.return_value = None

    # Mockar la respuesta de os.listdir() para simular una carpeta vacía
    with patch('os.listdir', return_value=[]):
        response = test_client.get(url_for('dataset.download_all_datasets'))

        assert response.status_code == 200
        assert b'\x00' in response.data
        assert len(response.data) == 22  # Header length


'''
def test_create_dataset_valid_form(test_client, mock_dataset_service, mock_zenodo_service):
    mock_service_instance = mock_dataset_service.return_value
    mock_service_instance.create_from_form.return_value = MagicMock(id=1, feature_models=[])
    mock_service_instance.move_feature_models.return_value = None

    response_data = {"id": 123, "conceptrecid": "456"}
    mock_zenodo_service.return_value.create_new_deposition.return_value = response_data

    response = test_client.post(url_for('dataset.create_dataset'), data={
        'title': 'Test Dataset',
        'upload_type': 'dataset',
        # Add other form fields here as required
    })

    assert response.status_code == 200
    assert response.json['message'] == "Everything works!"
    mock_service_instance.create_from_form.assert_called_once()
    mock_zenodo_service.return_value.create_new_deposition.assert_called_once()

def test_create_dataset_invalid_form(test_client):
    response = test_client.post(url_for('dataset.create_dataset'), data={})
    assert response.status_code == 400
    assert "message" in response.json

def test_list_datasets(test_client, mock_dataset_service):
    mock_service_instance = mock_dataset_service.return_value
    mock_service_instance.get_synchronized.return_value = [MagicMock(id=1), MagicMock(id=2)]

    response = test_client.get(url_for('dataset.list_datasets'))
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 2

def test_upload_invalid_file(test_client):
    response = test_client.post(url_for('dataset.upload'), data={"file": ("", "")})
    assert response.status_code == 400
    assert response.json['message'] == "No valid file"

def test_upload_valid_file(test_client):
    with patch('app.modules.dataset.routes.request.files') as mock_files:
        mock_file = MagicMock()
        mock_file.filename = 'test.uvl'
        mock_files.get.return_value = mock_file

        response = test_client.post(url_for('dataset.upload'))
        assert response.status_code == 200
        assert "message" in response.json

def test_download_dataset(test_client, mock_dataset_service):
    mock_service_instance = mock_dataset_service.return_value
    mock_service_instance.get_or_404.return_value = MagicMock(id=1, user_id=1)

    response = test_client.get(url_for('dataset.download_dataset', dataset_id=1))
    assert response.status_code == 200
    assert response.mimetype == 'application/zip'

def test_subdomain_index_redirect(test_client, mock_zenodo_service):
    mock_zenodo_service.return_value.get_new_doi.return_value = "10.1234/new-doi"

    response = test_client.get(url_for('dataset.subdomain_index', doi="10.1234/old-doi"))
    assert response.status_code == 302
    assert response.location.endswith("10.1234/new-doi")

def test_subdomain_index_not_found(test_client, mock_zenodo_service):
    mock_zenodo_service.return_value.get_new_doi.return_value = None

    response = test_client.get(url_for('dataset.subdomain_index', doi="10.1234/nonexistent"))
    assert response.status_code == 404

# Add more test cases for other routes as needed
'''
