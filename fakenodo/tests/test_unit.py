import pytest
from flask import url_for

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass

    yield test_client
    
def test_full_connection(test_client):
    response = test_client.get('/api/fakenodo/depositions')
    
    assert response.status_code == 200, response.request