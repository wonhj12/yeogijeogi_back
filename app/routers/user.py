from fastapi import APIRouter, Depends

from app.core.auth import get_uuid
from app.db.dao.user_dao import UserDAO
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


def get_user_service(user_id: str = Depends(get_uuid)):
    return UserService(UserDAO(user_id))


@router.post("/", status_code=201)
# 유저 등록
async def create_user(user_service: UserService = Depends(get_user_service)):
    await user_service.crerate_user()
    return {"message": "user-created"}
