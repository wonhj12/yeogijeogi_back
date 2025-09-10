from fastapi import HTTPException
from firebase_admin import auth


def check_token(token):
    return auth.verify_id_token(token)


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
        except Exception:
            print("Unknown error")
            raise HTTPException(status_code=500, detail="unknown-error")


def get_auth() -> FirebaseAuth:
    return FirebaseAuth()
