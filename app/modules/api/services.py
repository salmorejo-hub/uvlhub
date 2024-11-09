from app import db
import hashlib
import jwt
import os
import datetime

from app.modules.api.repositories import APIRepository
from core.services.BaseService import BaseService


def generateJWT(SECRET_KEY_JWT, user_id, expiration_date, now):
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

    def generate_token_with_validation(self, user_id, expiration_days):
        '''
        Genera un token JWT para el usuario especificado con validación de parámetros.
        '''
        try:
            expiration_days = int(expiration_days)
            if expiration_days <= 0:
                raise ValueError("Expiration must be a positive integer.")
        except (ValueError, TypeError) as e:
            return None, str(e)

        return self.generate_token(user_id, expiration_days)

    def generate_token(self, user_id, expiration_days):
        '''
        Genera el token sin realizar validaciones adicionales. Asume que `expiration_days` ya fue validado.
        '''
        try:
            SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
            now = datetime.datetime.now()
            expiration_date = now + datetime.timedelta(days=expiration_days)

            jwt_token = generateJWT(SECRET_KEY_JWT, user_id, expiration_date, now)

            api_token = self.create(
                token=hashlib.sha256(jwt_token.encode()).hexdigest(),
                user_id=int(user_id),
                expiration_date=expiration_date
            )

            db.session.add(api_token)
            db.session.commit()

            return jwt_token, None
        except Exception as exc:
            self.repository.session.rollback()
            return None, str(exc)
