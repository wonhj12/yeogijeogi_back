from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import get_uuid
from app.db.database import get_db
from app.services.course_service import CourseService


router = APIRouter(
    prefix="/course",
    tags=["course"],
)


def get_course_service(
    user_id: str = Depends(get_uuid),
    session: AsyncSession = Depends(get_db),
):
    return CourseService(user_id=user_id, session=session)


@router.get("/", status_code=200)
async def get_courses(course_service: CourseService = Depends(get_course_service)):
    courses = await course_service.get_courses()
    return courses
