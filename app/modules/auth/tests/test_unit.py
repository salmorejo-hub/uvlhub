import pytest
from flask import url_for
from app.modules.auth.models import User
from app.modules.auth.services import AuthenticationService
from app.modules.auth.repositories import UserRepository
from flask_mail import Mail
from app.modules.profile.repositories import UserProfileRepository


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


def test_login_success(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path != url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_login_unsuccessful_bad_email(test_client):
    response = test_client.post(
        "/login", data=dict(email="bademail@example.com", password="test1234"), follow_redirects=True
    )

    assert response.request.path == url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_login_unsuccessful_bad_password(test_client):
    response = test_client.post(
        "/login", data=dict(email="test@example.com", password="basspassword"), follow_redirects=True
    )

    assert response.request.path == url_for("auth.login"), "Login was unsuccessful"

    test_client.get("/logout", follow_redirects=True)


def test_remember_password_no_email(test_client):
    response = test_client.post(
        "/remember-my-password",
        data=dict(email=""),
        follow_redirects=True
    )

    assert response.request.path == url_for("auth.remember_my_password"), "Invalid email"
    assert b"This field is required" in response.data, response.data


def test_remember_password_bad_email(test_client):
    response = test_client.post(
        "/remember-my-password",
        data=dict(email="bademail@example.com"),
        follow_redirects=True
    )

    assert response.request.path == url_for("auth.remember_my_password"), "Invalid email"
    assert b"User not found" in response.data, response.data


def test_remember_password_succesful(test_client):
    response = test_client.post(
        "/remember-my-password",
        data=dict(email="bademail@example.com"),
        follow_redirects=True
    )

    assert response.request.path == url_for("auth.remember_my_password"), "Invalid email"


def test_signup_user_no_name(test_client):
    response = test_client.post(
        "/signup", data=dict(surname="Foo", email="test@example.com", password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert b"This field is required" in response.data, response.data



def test_signup_user_unsuccessful(test_client):
    email = "test@example.com"
    response = test_client.post(
        "/signup", data=dict(
            name="Test", 
            surname="Foo", 
            email=email, 
            password="test1234", 
            confirm_password="test1234"
        ), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert f"Email {email} in use".encode("utf-8") in response.data



def test_signup_user_successful(test_client):
    response = test_client.post(
        "/signup",
        data=dict(
            name="Foo",
            surname="Example", 
            email="foo@example.com", 
            password="foo1234",
            confirm_password="foo1234"), 
        follow_redirects=True,
    )
    assert response.request.path == url_for("auth.check_inbox"), "User was not redirected to the check-inbox page after sumbitting the form"


def test_service_create_with_profie_success(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "service_test@example.com",
        "password": "test1234"
    }

    AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 1
    assert UserProfileRepository().count() == 1


def test_service_create_with_profile_fail_no_email(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "",
        "password": "1234"
    }

    with pytest.raises(ValueError, match="Email is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


def test_service_create_with_profile_fail_no_password(clean_database):
    data = {
        "name": "Test",
        "surname": "Foo",
        "email": "test@example.com",
        "password": ""
    }

    with pytest.raises(ValueError, match="Password is required."):
        AuthenticationService().create_with_profile(**data)

    assert UserRepository().count() == 0
    assert UserProfileRepository().count() == 0


@pytest.fixture
def mail_outbox():
    mail = Mail()
    with mail.record_messages() as outbox:
        yield outbox

def test_signup_and_send_confirmation_email(test_client, mail_outbox):
    data = {
        "name": "Test",
        "surname": "User",
        "email": "testuser@example.com",
        "password": "testpassword",
        "confirm_password": "testpassword"
    }

    response = test_client.post(
        url_for('auth.show_signup_form'),
        data=data,
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"A confirmation email has been sent via email." in response.data

    # Verificar que se envió un correo electrónico
    assert len(mail_outbox) == 1
    assert mail_outbox[0].subject == "Please confirm your email"
    assert "testuser@example.com" in mail_outbox[0].recipients

    # Extraer el token del correo electrónico
    token = mail_outbox[0].body.split("token=")[1].split("\n")[0]

    return token


def test_confirm_email(test_client, mail_outbox):
    token = test_signup_and_send_confirmation_email(test_client, mail_outbox)

    response = test_client.get(
        url_for('auth.confirm_email', token=token),
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Your account has been confirmed." in response.data

    # Verificar que el usuario fue creado
    user = User.query.filter_by(email="testuser@example.com").first()
    assert user is not None
    assert user.is_active