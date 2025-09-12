from app.db.interface.walk_summary_interface import WalkSummaryInterface
from app.db.models.walks import Walks
from app.schemas.walk_schema.base_schema import UserWalkSummary


class WalkSummaryDAO(WalkSummaryInterface):
    async def get_user_walk_summary(self, user_id: str) -> UserWalkSummary:
        pipeline = [
            {"$match": {"user_id.$id": user_id}},
            {
                "$lookup": {
                    "from": "walk_summary",
                    "localField": "_id",
                    "foreignField": "walk_id.$id",
                    "as": "summary",
                }
            },
            {"$unwind": "$summary"},
            {
                "$group": {
                    "_id": "$user_id",
                    "walk_time": {"$sum": "$summary.time"},
                    "walk_distance": {"$sum": "$summary.distance"},
                }
            },
        ]
        cursor = Walks.get_pymongo_collection().aggregate(pipeline)
        summary = [doc async for doc in cursor]

        if not summary:
            return UserWalkSummary(walk_time=0, walk_distance=0.0)
        return UserWalkSummary(
            walk_time=summary[0].get("walk_time", 0),
            walk_distance=summary[0].get("walk_distance", 0.0),
        )
