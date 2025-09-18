from sqlalchemy import Integer, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models.users import Users
from app.db.models.walk_summaries import WalkSummaries
from app.db.models.walks import Walks


class UserRepository:
    async def get_by_id(self, session: AsyncSession, user_id: str) -> Users | None:
        """ID로 사용자 조회"""

        result = await session.execute(select(Users).where(Users.id == user_id))
        return result.scalars().first()

    async def create(self, session: AsyncSession, user_id: str) -> Users:
        """신규 사용자 생성"""

        new_user = Users(id=user_id)
        session.add(new_user)
        await session.commit()
        return new_user

    async def get_user(self, session: AsyncSession, user_id: str) -> tuple[int, int]:
        """사용자 산책 통계(총 거리, 총 시간) 조회"""

        result = await session.execute(
            select(
                func.cast(
                    func.floor(func.coalesce(func.sum(WalkSummaries.distance), 0)),
                    Integer,
                ),
                func.coalesce(func.sum(WalkSummaries.time), 0),
            )
            .join(Walks, WalkSummaries.walk_id == Walks.id)
            .where(Walks.user_id == user_id)
        )
        total_distance, total_time = result.one()
        return total_distance, total_time

    async def delete(self, session: AsyncSession, user: Users) -> None:
        """사용자 삭제"""

        await session.delete(user)
        await session.commit()
