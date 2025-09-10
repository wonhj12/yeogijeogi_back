from fastapi import HTTPException

from app.db.interface.user_interface import UserInterface
from app.db.models.users import Users


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
