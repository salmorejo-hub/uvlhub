from itsdangerous import SignatureExpired, URLSafeTimedSerializer
import pytest
from unittest.mock import patch
from flask import url_for, current_app
import secrets
from app.modules.auth.repositories import UserRepository
from app.modules.auth.services import AuthenticationService
from app.modules.profile.repositories import UserProfileRepository
from app import mail_service

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
    email = 'foo@example.com'
    response = test_client.post(
        "/signup",
        data=dict(
            name="Foo",
            surname="Example", 
            email=email, 
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



def test_email_confirmation(test_client, mocker):
    # Generar token
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps({'email': 'test7@example.com', 'password': 'password123', 'confirm_password': 'password123', 'name': 'Test', 'surname': 'User'}, salt='email-confirmation-salt')

    response = test_client.get(f'/confirm/{token}')

    # Verifica que se redirige correctamente
    assert response.status_code == 302
    assert response.headers["Location"] == "/email-confirmed"  # O el endpoint al que debe redirigir


def test_expired_token(test_client, mocker):
    # Generar token con expiración simulada
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps({'email': 'test7@example.com', 'password': 'password123', 'confirm_password': 'password123', 'name': 'Test', 'surname': 'User'}, salt='email-confirmation-salt')

    mocker.patch("app.modules.auth.routes.URLSafeTimedSerializer.loads", side_effect=SignatureExpired("Token expired"))

    response = test_client.get(f'/confirm/{token}')
    assert response.status_code == 302  # Redirige al formulario de registro
    assert response.headers["Location"] == url_for("auth.token_expired")


def test_invalid_token(test_client):
    invalid_token = "invalid-token"

    response = test_client.get(f'/confirm/{invalid_token}')
    assert response.status_code == 302  # Redirige al formulario de registro
    assert response.headers["Location"] == url_for("auth.invalid_token")

# def test_resend_confirmation_email(test_client, mocker):
#     mock_send_email = mocker.patch("app.mail_service.send_email")

#     response = test_client.post('/auth/resend-confirmation/', data={'email': 'test@example.com'})
#     assert response.status_code == 200
#     mock_send_email.assert_called_once()
#     assert b'A new confirmation email has been sent.' in response.data

def test_resend_confirmation_email_maximum_two_times(test_client):
    # Mockear el servicio de correo desde donde se usa en auth.routes
    with patch('app.modules.auth.routes.mail_service.send_email') as mock_send_email:
        # Datos de prueba para el signup
        signup_data = {
            'email': 'test8@example.com',
            'password': 'securepassword',
            'confirm_password': 'securepassword',
            'name': 'Test',
            'surname': 'User'
        }

        # Simular el formulario de signup
        response = test_client.post('/signup/', data=signup_data, follow_redirects=False)
        assert response.status_code == 302  # Redirección a /check-inbox/

        # Acceder a /check-inbox/ por primera vez (primer envío)
        response = test_client.get('/check-inbox/', follow_redirects=False)
        assert response.status_code == 200
        assert mock_send_email.call_count == 1, "El correo no fue enviado tras el primer acceso a /check-inbox/"

        # Acceder a /check-inbox/ por segunda vez (segundo envío)
        response = test_client.get('/check-inbox/', follow_redirects=False)
        assert response.status_code == 200
        assert mock_send_email.call_count == 2, "El correo no fue enviado tras el segundo acceso a /check-inbox/"

        # Intentar acceder a /check-inbox/ por tercera vez (no debe enviar correo)
        response = test_client.get('/check-inbox/', follow_redirects=False)
        assert response.status_code == 200
        assert mock_send_email.call_count == 2, "Algo falla: se envió un correo adicional después de alcanzar el límite"