from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    UserWithdrawalFailedException,
)
from app.core.firebase import get_auth
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema.response_schema import GetUserResDTO


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        session: AsyncSession,
    ):
        self.user_repository = user_repository
        self.session = session

    async def create_user(self, user_id: str) -> None:
        """Firebase UID를 기반으로 db에 사용자 등록"""

        user = await self.user_repository.get_by_id(self.session, user_id)
        if user:
            raise UserAlreadyExistsException()

        await self.user_repository.create(self.session, user_id)

    async def get_user(self, user_id: str) -> GetUserResDTO:
        """사용자 정보 조회 (총 산책 거리, 총 산책 시간)"""

        user = await self.user_repository.get_by_id(self.session, user_id)
        if not user:
            raise UserNotFoundException()

        total_distance, total_time = await self.user_repository.get_user(
            self.session, user_id
        )

        return GetUserResDTO(
            walk_distance=total_distance,
            walk_time=total_time,
        )

    async def delete_user(self, user_id: str) -> None:
        """사용자 및 관련 데이터 삭제"""

        user = await self.user_repository.get_by_id(self.session, user_id)
        if not user:
            raise UserNotFoundException()

        try:
            get_auth().delete_user(user_id)
            await self.user_repository.delete(self.session, user)
        except Exception as e:
            await self.session.rollback()
            raise UserWithdrawalFailedException(e=e)
