from sqlalchemy import (
    CheckConstraint,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class WalkSummaries(Base):
    """
    Attributes:
        walk_id (int): 산책 ID
        name (str): 산책 종료 장소 이름
        address (str): 산책 종료 장소 주소
        img_url (str): 산책 경로 이미지 URL
        time (int): 총 산책 시간 (분)
        distance (float): 총 산책 거리 (km)
        difficulty (int): 산책 난이도 (-5 ~ 5)
        mood (int): 산책 기분 (-5 ~ 5)
        memo (str): 산책 메모
        created_at (datetime): 산책 요약 생성 일시
    """

    __tablename__ = "walk_summaries"

    walk_id = Column(Integer, ForeignKey("walks.id"), primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
    time = Column(Integer, nullable=False)
    distance = Column(Float, nullable=False)
    difficulty = Column(Integer, nullable=False)
    mood = Column(Integer, nullable=False)
    memo = Column(String, default="", nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    walk = relationship("Walks", back_populates="walk_summaries")

    __table_args__ = (
        CheckConstraint(
            "difficulty >= -5 AND difficulty <= 5", name="difficulty_range"
        ),
        CheckConstraint("mood >= -5 AND mood <= 5", name="mood_range"),
    )
