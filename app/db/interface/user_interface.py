from abc import ABC, abstractmethod


class UserInterface(ABC):
    def __init__(self, user_id: str):
        self.user_id = user_id

    @abstractmethod
    async def check_user_exists(self) -> bool:
        pass

    @abstractmethod
    async def create_user(self) -> None:
        pass
