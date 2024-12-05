from flask_restful import Api
from app.modules.rating.api import init_blueprint_api
from core.blueprints.base_blueprint import BaseBlueprint

rating_bp = BaseBlueprint('rating', __name__, template_folder='templates')

api = Api(rating_bp)
init_blueprint_api(api)
