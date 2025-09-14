from fastapi import HTTPException
from firebase_admin import auth


def check_token(token):
    return auth.verify_id_token(token, clock_skew_seconds=5)


class FirebaseAuth:
    def verify_token(self, token):
        try:
            c = check_token(token)
            return c["user_id"]
        except auth.ExpiredIdTokenError:
            print("Token expired")
            raise HTTPException(status_code=401, detail="token-expired")
        except auth.RevokedIdTokenError:
            print("Token revoked")
            raise HTTPException(status_code=401, detail="token-revoked")
        except auth.InvalidIdTokenError:
            print("Invalid token")
            raise HTTPException(status_code=401, detail="invalid-token")
        except Exception as e:
            print("Unknown error:", e)
            raise HTTPException(status_code=500, detail="unknown-error")

    def delete_user(self, user_id):
        try:
            auth.delete_user(user_id)
        except auth.UserNotFoundError:
            print("User not found")
            raise HTTPException(status_code=404, detail="user-not-found")
        except Exception as e:
            print("Unknown error")
            raise HTTPException(status_code=500, detail="unknown-error")


def get_auth() -> FirebaseAuth:
    return FirebaseAuth()
