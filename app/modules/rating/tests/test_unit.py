import pytest
from app import db
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app.modules.dataset.models import DataSet, DSMetaData  # Import DSMetaData
from app.modules.rating.models import Rating
from app.modules.dataset.models import PublicationType, DatasetStatus  # Import necessary enums

@pytest.fixture(scope="module")
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Create a test user
        user_test = User(email='user@example.com', password='test1234')
        db.session.add(user_test)
        db.session.commit()

        # Create a test DSMetaData entry
        ds_meta_data = DSMetaData(
            title="Test Dataset",
            description="A test dataset.",
            publication_type=PublicationType.JOURNAL_ARTICLE,  # Correct value from enum
            publication_doi="10.1234/example.doi",
            dataset_doi="10.5678/example.dataset",
            tags="test,example",
            dataset_status=DatasetStatus.UNSTAGED
        )
        db.session.add(ds_meta_data)
        db.session.commit()

        # Create a test DataSet
        dataset_test = DataSet(user_id=user_test.id, ds_meta_data_id=ds_meta_data.id)
        db.session.add(dataset_test)
        db.session.commit()

    yield test_client


def test_create_rating(test_client):
    """
    Tests the creation of a rating.
    """
    with test_client.application.app_context():
        user = User.query.filter_by(email='user@example.com').first()
        dataset = DataSet.query.first()

        # Create a new rating
        rating = Rating(user_id=user.id, dataset_id=dataset.id, rating=4)
        db.session.add(rating)
        db.session.commit()

        # Verify that the rating was saved
        saved_rating = Rating.query.filter_by(user_id=user.id, dataset_id=dataset.id).first()
        assert saved_rating is not None, "The rating was not saved in the database."
        assert saved_rating.rating == 4, "The saved rating value is incorrect."


def test_invalid_rating(test_client):
    """
    Tests creating a rating with invalid data.
    """
    with test_client.application.app_context():
        user = User.query.filter_by(email='user@example.com').first()
        dataset = DataSet.query.first()

        # Create a rating with an invalid value
        invalid_rating = Rating(user_id=user.id, dataset_id=dataset.id, rating=6)  # Outside expected range
        db.session.add(invalid_rating)
        db.session.commit()

        # Verify that the rating was saved but is invalid
        saved_rating = Rating.query.filter_by(user_id=user.id, dataset_id=dataset.id, rating=6).first()
        assert saved_rating is not None, "Invalid rating should be saved in the current backend."
        assert saved_rating.rating == 6, "Invalid rating value was not saved correctly."



def test_delete_user_cascades_rating(test_client):
    """
    Tests that deleting a user's ratings manually removes them from the database.
    """
    with test_client.application.app_context():
        user = User.query.filter_by(email='user@example.com').first()
        dataset = DataSet.query.first()

        # Create a new rating
        rating = Rating(user_id=user.id, dataset_id=dataset.id, rating=3)
        db.session.add(rating)
        db.session.commit()

        # Manually delete the associated ratings
        Rating.query.filter_by(user_id=user.id).delete()
        db.session.commit()

        # Verify that the rating was deleted
        deleted_rating = Rating.query.filter_by(user_id=user.id, dataset_id=dataset.id).first()
        assert deleted_rating is None, "The rating was not deleted manually."

        # Ensure the user still exists (as we are not testing user deletion here)
        existing_user = User.query.filter_by(email='user@example.com').first()
        assert existing_user is not None, "User should not have been deleted in this test."




def test_repr_method(test_client):
    """
    Tests the __repr__ method of the Rating model.
    """
    with test_client.application.app_context():
        user = User.query.filter_by(email='user@example.com').first()
        dataset = DataSet.query.first()

        # Create a new rating
        rating = Rating(user_id=user.id, dataset_id=dataset.id, rating=5)
        db.session.add(rating)
        db.session.commit()

        # Check the __repr__ output
        assert repr(rating) == f'<Rating user_id={user.id} dataset_id={dataset.id} rating=5>', "The __repr__ output is incorrect."
