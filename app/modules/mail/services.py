import os

from dotenv import load_dotenv
from flask_mail import Mail, Message

from app.modules.mail.repositories import MailRepository
from core.services.BaseService import BaseService


class MailService(BaseService):

    def __init__(self):
        super().__init__(MailRepository())
        self.mail = None
        self.sender = None

    def init_app(self, app):
        load_dotenv()
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False
        app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'mail@domain.something')
        app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'password')
        app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
        self.mail = Mail(app)
        self.sender = app.config['MAIL_USERNAME']

    def send_reset_email(self, recipients, reset_url) -> None:
        subject = "Reset your password."
        body = self._build_body(reset_url)
        msg = Message(subject, sender=self.sender, recipients=recipients)
        msg.body = body
        self.mail.send(msg)

    def _build_body(self, reset_url) -> str:
        return f"""Hi there,\n
            It looks like you requested a password reset. No worries! Click the link below to reset your password:\n
            {reset_url}\n
            If you didn’t request a password reset, you can safely ignore this email.\n

            Best regards,\n
            The salmorejo-hub-1 Team"""
