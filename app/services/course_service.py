from fastapi import HTTPException
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.walk_points import WalkPoints
from app.db.models.walks import Walks
from app.schemas.course_schema.response_schema import CoursePreview, GetCoursesResDTO


class CourseService:
    def __init__(self, user_id: str, session: AsyncSession):
        self.user_id = user_id
        self.session = session

    async def get_courses(self):
        """코스 목록 조회"""

        try:
            subquery = select(
                WalkPoints.walk_id,
                WalkPoints.latitude,
                WalkPoints.longitude,
                func.row_number()
                .over(partition_by=WalkPoints.walk_id, order_by=desc(WalkPoints.id))
                .label("rn"),
            ).subquery("last_points")

            main_query = (
                select(
                    Walks.id.label("walk_id"),
                    subquery.c.latitude,
                    subquery.c.longitude,
                )
                .join(subquery, Walks.id == subquery.c.walk_id)
                .where(
                    Walks.user_id == self.user_id,
                    subquery.c.rn == 1,
                )
            )

            result = await self.session.execute(main_query)
            course_list = [CoursePreview(**row) for row in result.mappings().all()]
            return GetCoursesResDTO(courses=course_list)

        except Exception as e:
            print("Error fetching courses:", e)
            raise HTTPException(status_code=500, detail="course-fetch-failed")
