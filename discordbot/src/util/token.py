from src.database.models import UserToken


def get_token(user, session):
    db = session()
    try:
        message = None
        user_token = db.query(UserToken).filter(UserToken.user_id == str(user.id)).first()
        if user_token:
            return user_token.token
    except Exception as e:
        raise e
    finally:
        session.remove()