from beanie import BulkWriter
from fastapi import HTTPException

from app.db.interface.user_interface import UserInterface
from app.db.models.users import Users
from app.db.models.walk_points import WalkPoints
from app.db.models.walk_summary import WalkSummary
from app.db.models.walks import Walks


class UserDAO(UserInterface):
    def __init__(self, user_id: str):
        super().__init__(user_id)

    async def check_user_exists(self) -> bool:
        if await Users.get(self.user_id):
            return True
        return False

    async def create_user(self):
        if await self.check_user_exists():
            raise HTTPException(status_code=409, detail="user-already-exists")
        await Users(id=self.user_id).insert()

    async def delete_user(self) -> None:
        if not await self.check_user_exists():
            raise HTTPException(status_code=404, detail="user-not-found")

        user = await Users.find_one(Users.id == self.user_id)
        w_list = await Walks.find(Walks.user_id == user.id).to_list()

        async with BulkWriter() as bulk_writer:
            for w in w_list:
                wp_list = await WalkPoints.find(WalkPoints.walk_id == w).to_list()
                for wp in wp_list:
                    await wp.delete(bulk_writer=bulk_writer)

                ws_list = await WalkSummary.find(WalkSummary.walk_id == w).to_list()
                for ws in ws_list:
                    await ws.delete(bulk_writer=bulk_writer)

                await w.delete(bulk_writer=bulk_writer)

            await user.delete(bulk_writer=bulk_writer)
