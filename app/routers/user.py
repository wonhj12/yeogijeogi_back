from fastapi import APIRouter, Depends

from app.core.auth import get_uuid
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


# 유저 등록
@router.post("/", status_code=201)
async def create_user(
    user_id: str = Depends(get_uuid),
    user_service: UserService = Depends(UserService),
):
    await user_service.create_user(user_id)
    return {"message": "user-created"}


# 유저 정보 조회
@router.get("/", status_code=200)
async def get_user(
    user_id: str = Depends(get_uuid),
    user_service: UserService = Depends(UserService),
):
    user = await user_service.get_user(user_id)
    return user


# 유저 삭제
@router.delete("/", status_code=200)
async def delete_user(
    user_id: str = Depends(get_uuid),
    user_service: UserService = Depends(UserService),
):
    await user_service.delete_user(user_id)
    return {"message": "user-deleted"}
