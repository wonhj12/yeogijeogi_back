from beanie import Document, Link, Indexed
from pydantic import Field
from typing import Annotated
from datetime import datetime
import pymongo

from app.db.models.coordinate import Coordinate
from app.db.models.walks import Walks

"""
WalkPoints 객체 생성 예시
WalkPoints(
    walk_id=Walks 객체 id,
    location=Coordinate(coordinates=[longitude, latitude]),
    created_at=datetime.now()
)
"""


class WalkPoints(Document):
    index: int
    walk_id: Link[Walks]
    location: Annotated[Coordinate, Indexed(index_type=pymongo.GEOSPHERE)]
    created_at: datetime = Field(default_factory=datetime.now)


class Settings:
    name = "walk_points"
    indexes = [
        pymongo.IndexModel(
            [
                ("walk_id", pymongo.ASCENDING),
                ("index", pymongo.ASCENDING),
            ],
            unique=True,
        )
    ]
