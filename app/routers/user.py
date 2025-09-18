from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_uuid
from app.db.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    user_repository = UserRepository()
    return UserService(user_repository, session)


# 유저 등록
@router.post("/", status_code=201)
async def create_user(
    user_id: str = Depends(get_uuid),
    user_service: UserService = Depends(get_user_service),
):
    await user_service.create_user(user_id)
    return {"message": "user-created"}


# 유저 정보 조회
@router.get("/", status_code=200)
async def get_user(
    user_id: str = Depends(get_uuid),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_user(user_id)
    return user


# 유저 삭제
@router.delete("/", status_code=200)
async def delete_user(
    user_id: str = Depends(get_uuid),
    user_service: UserService = Depends(get_user_service),
):
    await user_service.delete_user(user_id)
    return {"message": "user-deleted"}
