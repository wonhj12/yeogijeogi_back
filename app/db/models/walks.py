from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Walks(Base):
    """
    Attributes:
        id (int): 산책 ID
        user_id (str): 사용자 ID
        name (str): 산책 시작 장소 이름
        address (str): 산책 시작 장소 주소
        time (int): 산책 예상 시간 (분)
        distance (float): 산책 예상 거리 (km)
        created_at (datetime): 산책 생성 일시
    """

    __tablename__ = "walks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    time = Column(Integer, nullable=False)
    distance = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("Users", back_populates="walks")
    walk_points = relationship(
        "WalkPoints", back_populates="walk", cascade="all, delete-orphan"
    )
    walk_summaries = relationship(
        "WalkSummaries",
        back_populates="walk",
        cascade="all, delete-orphan",
        uselist=False,
    )
