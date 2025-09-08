from beanie import Document, Link
from datetime import datetime
from pydantic import Field

from app.db.models.walks import Walks


class WalkSummary(Document):
    walk_id: Link[Walks]
    name: str  # 종료 지점 이름
    address: str  # 종료 지점 주소
    img_url: str
    time: int  # 실제 산책 시간 (분)
    distance: float  # 실제 산책 거리
    difficulty: int  # -5 ~ 5
    mood: int  # -5 ~ 5
    memo: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "walk_summary"
