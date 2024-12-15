import pytest
from unittest.mock import patch
from flask import url_for
from app import create_app
import os
from app.modules.dataset.routes import dataset_service


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


def test_download_all_datasets_error(test_client):
    with patch.object(dataset_service, 'zip_datasets', side_effect=Exception("Error al crear el ZIP")):
        response = test_client.get(url_for('dataset.download_all_datasets'))
        assert response.status_code == 500
        assert response.json['error'] == "Error al crear el ZIP"


@patch('os.remove')
def test_download_all_datasets_cleanup(mock_remove, test_client):
    response = test_client.get(url_for('dataset.download_all_datasets'))
    assert response.status_code == 200
    mock_remove.assert_called_once()