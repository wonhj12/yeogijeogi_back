from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class WalkPoints(Base):
    """
    Attributes:
        walk_id (int): 산책 ID
        index (int): 산책 경로 인덱스
        longitude (float): 경도
        latitude (float): 위도
        created_at (datetime): 생성 일시
    """

    __tablename__ = "walk_points"
    __table_args__ = (PrimaryKeyConstraint("walk_id", "index", name="pk_walkpoints"),)

    walk_id = Column(Integer, ForeignKey("walks.id"), nullable=False)
    index = Column(Integer, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    walk = relationship("Walks", back_populates="walk_points")
