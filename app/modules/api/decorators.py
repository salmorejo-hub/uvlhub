from functools import wraps
from flask import request, jsonify
import jwt
import os
from flask_login import login_user
from app.modules.auth.models import User

SECRET_KEY_JWT = os.getenv("SECRET_KEY_JWT")


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
            payload = jwt.decode(token, SECRET_KEY_JWT, algorithms=["HS256"])
            user_id = payload['user_id']
            user_email = payload.get('user_email')

            user = User.query.get(user_id)
            if user and user.email == user_email:
                login_user(user)
            else:
                return jsonify({'message': 'User authentication failed!'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated
