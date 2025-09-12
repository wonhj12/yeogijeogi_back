from abc import ABC, abstractmethod

from app.schemas.walk_schema.base_schema import UserWalkSummary


class WalkSummaryInterface(ABC):
    @abstractmethod
    async def get_user_walk_summary(self, user_id: str) -> UserWalkSummary:
        pass
