from fakenodo.app.routes import api_bp
# app/__init__.py
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        app.register_blueprint(api_bp)

    return app
