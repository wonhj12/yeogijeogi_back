from beanie import Document
from pydantic import Field


class Users(Document):
    id: str = Field(alias="_id")


class Settings:
    name = "users"
