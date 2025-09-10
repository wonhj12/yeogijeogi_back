from app.core.firebase import get_auth
from app.db.interface.user_interface import UserInterface


class UserService:
    def __init__(self, user_database: UserInterface):
        self.user_database = user_database

    async def create_user(self) -> None:
        await self.user_database.create_user()
