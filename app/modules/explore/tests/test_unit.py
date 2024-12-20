
import pytest
from app.modules.explore.services import ExploreService
from app.modules.auth.seeders import AuthSeeder
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


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


def test_filtering_service_model_count(test_client):
    """
    Test to verify that the filtering service correctly counts the number of datasets based on the number of models.
    """
    explore_service = ExploreService()
    datasets = explore_service.filter(min_number_of_models=10, max_number_of_models=60)
    expected_dataset_count = 1  # Based on the entries in seeders.py (50 and 75 models)
    assert len(datasets) == expected_dataset_count, \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"


def test_filtering_service_feature_count(test_client):
    """
    Test to verify that the filtering service correctly counts the number of datasets based on the number of features.
    """
    explore_service = ExploreService()
    datasets = explore_service.filter(min_number_of_features=10, max_number_of_features=30)
    expected_dataset_count = 3  # Based on the entries in seeders.py (10, 20, and 30 features)
    assert len(datasets) == expected_dataset_count, \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"


def test_filtering_service_model_and_feature_count(test_client):
    """
    Test to verify that the filtering service correctly counts the number of
    datasets based on the number of models and
    features.
    """
    explore_service = ExploreService()
    datasets = explore_service.filter(min_number_of_models=20, max_number_of_models=100,
                                      min_number_of_features=0,
                                      max_number_of_features=30)
    # Based on the entries in seeders.py (50 models, 20 features and 75 models, 40 features)
    expected_dataset_count = 2
    assert len(datasets) == expected_dataset_count, \
        \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"


def test_filtering_service_by_year(test_client):
    """
    Test to verify that the filtering service correctly filters datasets by year.
    """
    explore_service = ExploreService()
    datasets = explore_service.filter(year="2021")
    expected_dataset_count = 2  # Datasets created in 2021 (15th Jan, 20th Jun)
    assert len(datasets) == expected_dataset_count, \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"


def test_filtering_service_by_month(test_client):
    """
    Test to verify that the filtering service correctly filters datasets by month.
    """
    explore_service = ExploreService()
    datasets = explore_service.filter(year="2021", month="06")
    expected_dataset_count = 1  # Dataset created in June 2021
    assert len(datasets) == expected_dataset_count, \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"


def test_filtering_service_by_day(test_client):
    """
    Test to verify that the filtering service correctly filters datasets by specific day.
    """
    explore_service = ExploreService()
    datasets = explore_service.filter(year="2021", month="01", day="15")
    expected_dataset_count = 1  # Dataset created on 15th January 2021
    assert len(datasets) == expected_dataset_count, \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"


def test_filtering_service_max_size_kb(test_client):
    """
    Test to verify that the filtering service correctly counts the number of datasets based on the maximum size in KB.
    """
    explore_service = ExploreService()
    max_size = 38
    datasets = explore_service.filter(max_size=max_size, size_unit="kb")
    expected_dataset_count = 2  # Based on the entries in seeders.py (500 bytes)
    assert len(datasets) == expected_dataset_count, \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"


def test_filtering_service_max_size_mb(test_client):
    """
    Test to verify that the filtering service correctly counts the number of datasets based on the maximum size in MB.
    """
    explore_service = ExploreService()
    max_size = 10
    datasets = explore_service.filter(max_size=max_size, size_unit="mb")
    expected_dataset_count = 4
    assert len(datasets) == expected_dataset_count, \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"


def test_filtering_service_max_size_gb(test_client):
    """
    Test to verify that the filtering service correctly counts the number of datasets based on the maximum size in GB.
    """
    explore_service = ExploreService()
    max_size = 0.00005
    datasets = explore_service.filter(max_size=max_size, size_unit="gb")
    expected_dataset_count = 2  # Based on the entries in seeders.py (all datasets)
    assert len(datasets) == expected_dataset_count, \
        f"Expected {expected_dataset_count} datasets, but got {len(datasets)}"
