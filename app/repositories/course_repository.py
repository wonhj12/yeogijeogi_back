from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from app.db.models.walk_points import WalkPoints
from app.db.models.walks import Walks


class CourseRepository:
    async def get_courses_with_last_point_by_user_id(
        self, session: AsyncSession, user_id: str
    ) -> Result:
        """사용자의 모든 코스와 각 코스의 마지막 지점을 조회"""

        subquery = (
            select(
                WalkPoints.walk_id,
                WalkPoints.latitude,
                WalkPoints.longitude,
                func.row_number()
                .over(partition_by=WalkPoints.walk_id, order_by=desc(WalkPoints.id))
                .label("rn"),
            )
            .select_from(WalkPoints)
            .subquery("last_points")
        )

        main_query = (
            select(
                Walks.id.label("walk_id"),
                subquery.c.latitude,
                subquery.c.longitude,
            )
            .join(subquery, Walks.id == subquery.c.walk_id)
            .where(
                Walks.user_id == user_id,
                subquery.c.rn == 1,
            )
        )

        result = await session.execute(main_query)
        return result
