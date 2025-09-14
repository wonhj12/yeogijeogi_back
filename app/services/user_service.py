from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.firebase import get_auth
from app.db.models.users import Users
from app.db.models.walk_summaries import WalkSummaries
from app.db.models.walks import Walks
from app.schemas.user_schema.response_schema import GetUserResDTO


class UserService:
    def __init__(self, user_id: str, session: AsyncSession):
        self.user_id = user_id
        self.session = session

    async def _check_user_exists(self) -> Users | None:
        """DB에 사용자가 존재하는지 확인, 없으면 HTTPException 발생"""

        result = await self.session.execute(
            select(Users).where(Users.id == self.user_id)
        )
        user = result.scalars().first()
        if not user:
            return None
        return user

    async def create_user(self) -> None:
        """Firebase UID를 기반으로 db에 사용자 등록"""

        user = await self._check_user_exists()
        if user:
            raise HTTPException(status_code=409, detail="user-already-exists")

        new_user = Users(id=self.user_id)
        self.session.add(new_user)
        await self.session.commit()

    async def get_user(self) -> GetUserResDTO:
        """사용자 정보 조회 (총 산책 거리, 총 산책 시간)"""
        user = await self._check_user_exists()
        if not user:
            raise HTTPException(status_code=404, detail="user-not-found")

        result = await self.session.execute(
            select(
                func.coalesce(func.sum(WalkSummaries.distance), 0),
                func.coalesce(func.sum(WalkSummaries.time), 0),
            )
            .join(Walks, WalkSummaries.walk_id == Walks.id)
            .where(Walks.user_id == self.user_id)
        )

        total_distance, total_time = result.one()

        return GetUserResDTO(
            walk_distance=total_distance,
            walk_time=total_time,
        )

    async def delete_user(self) -> None:
        """사용자 및 관련 데이터 삭제"""

        user = await self._check_user_exists()
        if not user:
            raise HTTPException(status_code=404, detail="user-not-found")

        try:
            get_auth().delete_user(self.user_id)
            await self.session.delete(user)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="user-withdrawal-failed")
