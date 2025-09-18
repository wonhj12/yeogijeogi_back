from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class WalkPoints(Base):
    """
    산책 경로의 각 지점 정보를 저장하는 모델.

    - `index` 컬럼을 삭제하고, 자동 증가하는 `id`를 기본 키(PK)로 사용합니다.
    - 데이터가 삽입된 순서가 `id`를 통해 보장됩니다.

    Attributes:
        id (int): 고유 ID (PK, 자동 증가)
        walk_id (int): 산책 ID (FK)
        longitude (float): 경도
        latitude (float): 위도
        created_at (datetime): 생성 일시
    """

    __tablename__ = "walk_points"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    walk_id = Column(Integer, ForeignKey("walks.id"), nullable=False, index=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    walk = relationship("Walks", back_populates="walk_points")
