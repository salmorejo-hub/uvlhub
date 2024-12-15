import secrets

import pytest
from flask import url_for

from app.modules.auth.repositories import UserRepository
from app.modules.auth.services import AuthenticationService
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
        data=dict(email="test@example.com"),
        follow_redirects=True
    )

    assert response.request.path == url_for("auth.remember_my_password"), "Invalid email"
    assert b"Mail succesfully sent" in response.data, response.data


def test_reset_password_bad_token(test_client):
    response = test_client.get("/reset-password/badtoken", follow_redirects=True)

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    assert b"Page Not Found" in response.data, "404 error page not displayed"


def test_reset_password_succesful(test_client):
    authentication_service = AuthenticationService()

    email = "test@example.com"
    token = authentication_service.generate_reset_token(email)
    response = test_client.get(f"/reset-password/{token}")

    assert response.status_code == 200
    assert b"Reset password" in response.data, response.data

    new_password = secrets.token_urlsafe(16)
    response = test_client.post(
        f"/reset-password/{token}",
        data=dict(password=new_password),
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert url_for("auth.login") in response.request.path, response.data


def test_signup_user_no_name(test_client):
    response = test_client.post(
        "/signup", data=dict(surname="Foo", email="test@example.com", password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert b"This field is required" in response.data, response.data


def test_signup_user_unsuccessful(test_client):
    email = "test@example.com"
    response = test_client.post(
        "/signup", data=dict(name="Test", surname="Foo", email=email, password="test1234"), follow_redirects=True
    )
    assert response.request.path == url_for("auth.show_signup_form"), "Signup was unsuccessful"
    assert f"Email {email} in use".encode("utf-8") in response.data


def test_signup_user_successful(test_client):
    response = test_client.post(
        "/signup",
        data=dict(name="Foo", surname="Example", email="foo@example.com", password="foo1234"),
        follow_redirects=True,
    )
    assert response.request.path == url_for("public.index"), "Signup was unsuccessful"


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
