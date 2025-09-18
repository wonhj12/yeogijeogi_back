from firebase_admin import auth

from app.core.exceptions import (
    InvalidTokenException,
    TokenExpiredException,
    TokenRevokedException,
    UnknownErrorException,
    UserNotFoundException,
)


def check_token(token):
    return auth.verify_id_token(token, clock_skew_seconds=5)


class FirebaseAuth:
    def verify_token(self, token):
        try:
            c = check_token(token)
            return c["user_id"]
        except auth.ExpiredIdTokenError as e:
            raise TokenExpiredException(e=e)
        except auth.RevokedIdTokenError as e:
            raise TokenRevokedException(e=e)
        except auth.InvalidIdTokenError as e:
            raise InvalidTokenException(e=e)
        except Exception as e:
            raise UnknownErrorException(e=e)

    def delete_user(self, user_id):
        try:
            auth.delete_user(user_id)
        except auth.UserNotFoundError as e:
            raise UserNotFoundException(e=e)
        except Exception as e:
            raise UnknownErrorException(e=e)


def get_auth() -> FirebaseAuth:
    return FirebaseAuth()
