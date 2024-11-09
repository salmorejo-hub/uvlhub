from flask import (abort, app, current_app, flash, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_user, logout_user
from itsdangerous import URLSafeTimedSerializer

from app import mail_service
from app.modules.auth import auth_bp
from app.modules.auth.forms import (LoginForm, RememberMyPasswordForm,
                                    ResetPasswordForm, SignupForm)
from app.modules.auth.models import User
from app.modules.auth.services import AuthenticationService
from app.modules.mail.services import MailService
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
        if not authentication_service.is_email_available(email):
            return render_template("auth/signup_form.html", form=form, error=f'Email {email} in use')

        try:
            user = authentication_service.create_with_profile(**form.data)
        except Exception as exc:
            return render_template("auth/signup_form.html", form=form, error=f'Error creating user: {exc}')

        # Log user
        login_user(user, remember=True)
        return redirect(url_for('public.index'))

    return render_template("auth/signup_form.html", form=form)


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
        else:
            return render_template('auth/remember_my_password.html', form=form, error='Not user found')
    
    print(form.errors)
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
