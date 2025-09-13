from sqlalchemy import Column, String


from app.db.database import Base


class Users(Base):
    """
    Attributes:
        id (str): Firebase UID
    """

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
