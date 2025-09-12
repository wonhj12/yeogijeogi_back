from pydantic import BaseModel


class UserWalkSummary(BaseModel):
    walk_distance: float  # 총 산책 거리 (km 단위)
    walk_time: int  # 총 산책 시간 (분 단위)
