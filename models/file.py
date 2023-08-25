from beanie import Document,Link
from .user import UserModel

class FileModel(Document):
    filename: str
    content_type: str
    path: str
    user:Link[UserModel]

    class Settings:
        name = "file"
