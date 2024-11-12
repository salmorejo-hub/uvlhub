from functools import wraps
from flask import request, jsonify
import jwt
import os
import hashlib

from flask_login import login_user
from app.modules.auth.models import User
from app.modules.api.models import APIToken


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if "Bearer" in auth_header else None

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")
            data = jwt.decode(token, SECRET_KEY_JWT, algorithms=["HS256"])
            user_id = data['user_id']

            hashed_token = hashlib.sha256(token.encode()).hexdigest()
            api_token = APIToken.query.filter_by(token=hashed_token, user_id=user_id).first()

            if not api_token or api_token.is_expired():
                return jsonify({'message': 'Token is invalid or has expired!'}), 401

            user = User.query.get(user_id)
            if user:
                login_user(user)

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated
