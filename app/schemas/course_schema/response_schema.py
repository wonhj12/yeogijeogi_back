from pydantic import BaseModel


class CoursePreview(BaseModel):
    walk_id: int
    longitude: float
    latitude: float


class GetCoursesResDTO(BaseModel):
    courses: list[CoursePreview]
