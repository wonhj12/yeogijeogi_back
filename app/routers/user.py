from fastapi import APIRouter, Depends

from app.core.auth import get_uuid
from app.db.dao.user_dao import UserDAO
from app.db.dao.walk_summary_dao import WalkSummaryDAO
from app.services.user_service import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


def get_user_service(user_id: str = Depends(get_uuid)):
    return UserService(UserDAO(user_id), WalkSummaryDAO())


# 유저 등록
@router.post("/", status_code=201)
async def create_user(user_service: UserService = Depends(get_user_service)):
    await user_service.create_user()
    return {"message": "user-created"}


# 유저 정보 조회
@router.get("/", status_code=200)
async def get_user(user_service: UserService = Depends(get_user_service)):
    user = await user_service.get_user()
    return user
