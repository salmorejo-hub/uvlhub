import pytest
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
