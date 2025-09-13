from app.core.firebase import get_auth
from app.db.interface.user_interface import UserInterface
from app.db.interface.walk_summary_interface import WalkSummaryInterface
from app.schemas.user_schema.response_schema import GetUserResDTO


class UserService:
    def __init__(
        self,
        user_interface: UserInterface,
        walk_summary_interface: WalkSummaryInterface,
    ):
        self.user_interface = user_interface
        self.walk_summary_interface = walk_summary_interface

    async def create_user(self) -> None:
        await self.user_interface.create_user()

    async def get_user(self) -> GetUserResDTO:
        summary = await self.walk_summary_interface.get_user_walk_summary(
            self.user_interface.user_id
        )
        return GetUserResDTO(
            walk_distance=summary.walk_distance,
            walk_time=summary.walk_time,
        )

    async def delete_user(self) -> None:
        await self.user_interface.delete_user()
        get_auth().delete_user(self.user_interface.user_id)
