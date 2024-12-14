from unittest.mock import MagicMock, patch
import pytest
from app.modules.auth.seeders import AuthSeeder
from app.modules.exploreuvl.services import ExploreServiceUvl
from app.modules.dataset.seeders import DataSetSeeder


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        users = AuthSeeder()
        users.run()

        seeder = DataSetSeeder()
        seeder.run()

    yield test_client

# Unit test


@pytest.fixture
def exploreuvl_service():
    return ExploreServiceUvl()


def test_filter(exploreuvl_service):
    with patch.object(exploreuvl_service.repository, 'filter') as mock_filter:
        mock_fm = [MagicMock(id=1), MagicMock(id=2), MagicMock(id=3)]
        mock_filter.return_value = mock_fm

        query = ""
        title = ""
        description = ""
        authors = ""
        q_tags = ""
        bytes = ""
        publication_type = "any"
        tags = []
        advanced_search = exploreuvl_service.filter(
            query, title, description, authors, q_tags, bytes, publication_type, tags)

        assert advanced_search == mock_fm
        assert len(advanced_search) == 3
        mock_filter.assert_called_with(query, title, description, authors, q_tags, bytes, publication_type, tags)

        query = "any"
        normal_search = exploreuvl_service.filter(
            query, title, description, authors, q_tags, bytes, publication_type, tags)

        assert normal_search == mock_fm
        assert len(normal_search) == 3
        mock_filter.assert_called_with(query, title, description, authors, q_tags, bytes, publication_type, tags)

# Integration test


def test_access_filter(test_client):

    response = test_client.get(f'/exploreuvl?query=')
    assert response.status_code == 200, "The page could not be accessed."

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 12, "The response doesn't have the expected data"


def test_basic_filter_positive(test_client):

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '6',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 2, "The response doesn't have the expected data"
    assert b'Feature Model 6' in response.data, "Object (6) expected in the search"
    assert b'Feature Model 7' in response.data, "Object (7) expected in the search"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'softwaredocumentation'
    }, follow_redirects=True)

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 12, "The response doesn't have the expected data"


def test_basic_filter_negative(test_client):

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': 'no one',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 0, "The response doesn't have the expected result"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '1',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'taxonomictreatment'
    }, follow_redirects=True)

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 0, "The response doesn't have the expected result"


def test_advanced_filter_positive(test_client):

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '1',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 4, "The response doesn't have the expected data"
    assert b'Feature Model 1' in response.data, "Object (1) expected in the search"
    assert b'Feature Model 10' in response.data, "Object (10) expected in the search"
    assert b'Feature Model 11' in response.data, "Object (11) expected in the search"
    assert b'Feature Model 12' in response.data, "Object (12) expected in the search"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '2',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 2, "The response doesn't have the expected data"
    assert b'Description for feature model 2' in response.data, "Object (2) expected in the search"
    assert b'Description for feature model 12' in response.data, "Object (12) expected in the search"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '',
        'authors': '6',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 2, "The response doesn't have the expected data"
    assert b'Author 6' in response.data, "Object (6) expected in the search"
    assert b'0000-0000-0000-1006' in response.data, "Object (7) expected in the search"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': 'tag1 tag2',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 12, "The response doesn't have the expected data"
    assert b'tag1' in response.data, "Object (6) expected in the search"
    assert b'tag2' in response.data, "Object (7) expected in the search"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': 3000,
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 2, "The response doesn't have the expected data"
    assert b'1024' in response.data, "Object (1) expected in the search"
    assert b'2048' in response.data, "Object (2) expected in the search"


def test_advanced_filter_negative(test_client):

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': 'no one',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 0, "The response doesn't have the expected result"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': 'no one',
        'authors': '',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 0, "The response doesn't have the expected result"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '',
        'authors': 'no one',
        'q_tags': '',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 0, "The response doesn't have the expected result"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': 'no one',
        'bytes': '',
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 0, "The response doesn't have the expected result"

    response = test_client.post('/exploreuvl', json={
        'csrf_token': 'TestToken',
        'query': '',
        'title': '',
        'description': '',
        'authors': '',
        'q_tags': '',
        'bytes': 0,
        'publication_type': 'any'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list), "The response data can't be accesed"
    assert len(data) == 0, "The response doesn't have the expected result"
