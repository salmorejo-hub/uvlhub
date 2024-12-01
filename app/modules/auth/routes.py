from flask import abort, current_app, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_user, logout_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import logging

from app import mail_service
from app.modules.auth import auth_bp
from app.modules.auth.forms import (LoginForm, RememberMyPasswordForm,
                                    ResetPasswordForm, SignupForm)
from app.modules.auth.models import User
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()

@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data
        if not authentication_service.is_email_available(email):
            return render_template("auth/signup_form.html", form=form, error=f'Email {email} in use')

        # Generate a token for email verification
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps({'email': email, 'password': password, 'name': name, 'surname': surname}, salt='email-confirmation-salt')
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('auth/activate.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        mail_service.send_email(subject, recipients=[email], html_body=html)

        flash('A confirmation email has been sent via email.', 'success')
        return redirect(url_for('auth.check_inbox'))

    return render_template("auth/signup_form.html", form=form)

@auth_bp.route('/check-inbox')
def check_inbox():
    return render_template("auth/check_inbox.html")

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        data = serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
        email = data['email']
        password = data['password']
        name = data['name']
        surname = data['surname']
    except SignatureExpired:
        flash('The confirmation link has expired.', 'danger')
        return redirect(url_for('auth.show_signup_form'))
    except BadSignature:
        flash('The confirmation link is invalid.', 'danger')
        return redirect(url_for('auth.show_signup_form'))
    except Exception as e:
        logging.error(f"Error confirming email: {e}")
        flash('An error occurred while confirming your email.', 'danger')
        return redirect(url_for('auth.show_signup_form'))

    if not authentication_service.is_email_available(email):
        flash('Email already confirmed. Please login.', 'success')
        return redirect(url_for('auth.login'))

    # Create the user with the provided data
    try:
        user = authentication_service.create_with_profile(email=email, password=password, name=name, surname=surname)
        login_user(user, remember=True)
        flash('Your account has been confirmed.', 'success')
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        flash('An error occurred while creating your account.', 'danger')
        return redirect(url_for('auth.show_signup_form'))

    return redirect(url_for('auth.email_confirmed'))

@auth_bp.route('/email-confirmed')
def email_confirmed():
    return render_template("auth/email_confirmed.html")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        if authentication_service.login(form.email.data, form.password.data):
            return redirect(url_for('public.index'))

        return render_template("auth/login_form.html", form=form, error='Invalid credentials')

    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/remember-my-password', methods=['GET', 'POST'])
def remember_my_password():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    form = RememberMyPasswordForm()

    # Idk why the second time you try a POST validate_on_submit returns False
    if request.method == 'POST' and form.validate_on_submit():
        user_email = form.email.data
        user = User.query.filter_by(email=user_email).first()
        if user:
            token = authentication_service.generate_reset_token(user.email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            mail_service.send_reset_email(recipients=[user_email], reset_url=reset_url)
            return render_template('auth/mail_sent.html')
        return render_template('auth/remember_my_password.html', form=form, error='User not found')

    return render_template('auth/remember_my_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).loads(
            token, salt='password-reset-salt', max_age=3600
        )
    except Exception:
        return abort(404)

    form = ResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            password = form.password.data
            authentication_service.reset_password(user, password)
            return redirect(url_for('auth.login'))

        return render_template('auth/reset_password.html', form=form, error='Something went wrong')
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))
