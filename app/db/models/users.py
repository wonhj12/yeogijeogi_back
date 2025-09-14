from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Users(Base):
    """
    Attributes:
        id (str): Firebase UID
    """

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)

    walks = relationship("Walks", back_populates="user", cascade="all, delete-orphan")
