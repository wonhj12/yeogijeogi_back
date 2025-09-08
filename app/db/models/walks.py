from beanie import Document, BeanieObjectId, Link
from datetime import datetime
from pydantic import Field

from app.db.models.users import Users


class Walks(Document):
    _id: BeanieObjectId
    user_id: Link[Users]
    name: str  # 시작
    address: str  # 시작 지점 주소
    time: int  # 예상 산책 시간
    distance: float  # 예상 산책 거리
    created_at: datetime = Field(default_factory=datetime.now)


class Settings:
    name = "walks"
