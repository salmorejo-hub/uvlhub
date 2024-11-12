import jwt
import os
import datetime

from app.modules.api.repositories import APIRepository
from core.services.BaseService import BaseService

# SE USA UTC COMO ZONA HORARIA PARA ESTANDARIZAR LA GENERACIÓN DE FECHAS

SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")


def generateJWT(SECRET_KEY_JWT, user_id, expiration_days):
    now = datetime.datetime.now(datetime.timezone.utc)
    expiration_date = now + datetime.timedelta(days=expiration_days)
    payload = {
        'user_id': user_id,
        'exp': expiration_date,
        'iat': now
    }
    token = jwt.encode(payload, SECRET_KEY_JWT, algorithm='HS256')
    return token


class APITokenService(BaseService):
    def __init__(self):
        super().__init__(APIRepository())

    def generate_token(self, user_id, expiration_days):
        try:
            expiration_days = int(expiration_days)
            if expiration_days <= 0:
                raise ValueError("Expiration must be a positive integer.")

            jwt_token = generateJWT(SECRET_KEY_JWT, user_id, expiration_days)
            return jwt_token, None
        except (ValueError, TypeError) as e:
            return None, str(e)