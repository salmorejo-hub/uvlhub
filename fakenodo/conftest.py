# conftest.py en la raíz del proyecto (uvlhub/)
import pytest
from flask import Flask

@pytest.fixture(scope="module")
def test_client():
    app = Flask(__name__)
    app.config["testing"] = True
    with app.test_client() as client:
        yield client
