import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class BaseCustomException(HTTPException):
    def __init__(self, status_code: int, detail: str, e: Exception | None = None):
        log_message = f"{detail}"
        if e:
            log_message += f", Error: {e}"

        logger.error(log_message)
        super().__init__(status_code=status_code, detail=detail)


class InvalidTokenException(BaseCustomException):
    def __init__(self, e: Exception | None = None):
        super().__init__(status_code=401, detail="invalid-token", e=e)


class TokenExpiredException(BaseCustomException):
    def __init__(self, e: Exception | None = None):
        super().__init__(status_code=401, detail="token-expired", e=e)


class TokenRevokedException(BaseCustomException):
    def __init__(self, e: Exception | None = None):
        super().__init__(status_code=401, detail="token-revoked", e=e)


class UserNotFoundException(BaseCustomException):
    def __init__(self, e: Exception | None = None):
        super().__init__(status_code=404, detail="user-not-found", e=e)


class UserAlreadyExistsException(BaseCustomException):
    def __init__(self, e: Exception | None = None):
        super().__init__(status_code=409, detail="user-already-exists", e=e)


class UnknownErrorException(BaseCustomException):
    def __init__(self, e: Exception | None = None):
        super().__init__(status_code=500, detail="unknown-error", e=e)


class CourseFetchFailedException(BaseCustomException):
    def __init__(self, e: Exception | None = None):
        super().__init__(status_code=500, detail="course-fetch-failed", e=e)


class UserWithdrawalFailedException(BaseCustomException):
    def __init__(self, e: Exception | None = None):
        super().__init__(status_code=500, detail="user-withdrawal-failed", e=e)
