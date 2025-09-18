from fastapi import APIRouter, Depends

from app.core.auth import get_uuid
from app.services.course_service import CourseService


router = APIRouter(
    prefix="/course",
    tags=["course"],
)


@router.get("/", status_code=200)
async def get_courses(
    user_id: str = Depends(get_uuid),
    course_service: CourseService = Depends(CourseService),
):
    courses = await course_service.get_courses(user_id)
    return courses
