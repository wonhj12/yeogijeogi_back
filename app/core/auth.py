from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends

from app.core.exceptions import InvalidTokenException
from app.core.firebase import get_auth

security = HTTPBearer(auto_error=False)


def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise InvalidTokenException()
    return credentials.credentials


def get_uuid(token: str = Depends(get_token), auth=Depends(get_auth)):
    return auth.verify_token(token)
