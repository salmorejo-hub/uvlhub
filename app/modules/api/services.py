from app import db
import hashlib
import jwt
import os
import datetime

from app.modules.api.repositories import APIRepository
from core.services.BaseService import BaseService

# SE USA UTC COMO ZONA HORARIA PARA ESTANDARIZAR LA GENERACIÓN DE FECHAS


def generateJWT(SECRET_KEY_JWT, user_id, expiration_days):
    now = datetime.datetime.now(datetime.timezone.utc)
    expiration_date = now + datetime.timedelta(minutes=expiration_days)
    payload = {
        'user_id': user_id,
        'exp': expiration_date,
        'iat': now
    }
    token = jwt.encode(payload, SECRET_KEY_JWT, algorithm='HS256')
    return token, expiration_date, now


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

        token, error = self.generate_token(user_id, expiration_days)
        return token, error

    def generate_token(self, user_id, expiration_days):
        '''
        Genera el token sin realizar validaciones adicionales. Asume que `expiration_days` ya fue validado.
        '''
        try:
            SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")

            jwt_token, exp_date, created = generateJWT(SECRET_KEY_JWT, user_id, expiration_days)

            api_token = self.create(
                token=hashlib.sha256(jwt_token.encode()).hexdigest(),
                user_id=int(user_id),
                expiration_date=exp_date,
                created_at=created
            )

            db.session.add(api_token)
            db.session.commit()

            return jwt_token, None
        except Exception as exc:
            self.repository.session.rollback()
            return None, str(exc)
