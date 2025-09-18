from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.repositories.course_repository import CourseRepository
from app.schemas.course_schema.response_schema import CoursePreview, GetCoursesResDTO


class CourseService:
    def __init__(
        self,
        course_repository: CourseRepository = Depends(),
        session: AsyncSession = Depends(get_db),
    ):
        self.course_repo = course_repository
        self.session = session

    async def get_courses(self, user_id: str) -> GetCoursesResDTO:
        """코스 목록 조회"""

        try:
            result = await self.course_repo.get_courses_with_last_point_by_user_id(
                self.session, user_id
            )
            course_list = [CoursePreview(**row) for row in result.mappings().all()]
            return GetCoursesResDTO(courses=course_list)

        except Exception as e:
            print("Error fetching courses:", e)
            raise HTTPException(status_code=500, detail="course-fetch-failed")
