from beanie import Document, Link
from pydantic import BaseModel
from .user import UserModel


class InsightInputModel(BaseModel):
    name: str
    settingData: str
    mtag: str
    rtag: str
    description: str
    access: bool
    image: str
    canvas: str


class InsightModel(Document, InsightInputModel):
    user: Link[UserModel]

    class Settings:
        name = "insight"
