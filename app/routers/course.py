from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_uuid
from app.db.database import get_db
from app.repositories.course_repository import CourseRepository
from app.services.course_service import CourseService


router = APIRouter(
    prefix="/course",
    tags=["course"],
)


def get_course_service(session: AsyncSession = Depends(get_db)) -> CourseService:
    course_repository = CourseRepository()
    return CourseService(course_repository, session)


@router.get("/", status_code=200)
async def get_courses(
    user_id: str = Depends(get_uuid),
    course_service: CourseService = Depends(get_course_service),
):
    courses = await course_service.get_courses(user_id)
    return courses
