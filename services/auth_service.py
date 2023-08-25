from schemas import User


class AuthService:
    def __init__(self):
        pass

    async def get_user(self, username: str) -> User:
        user = await User.find_one(User.username == username)
        return user
        # user = await db["user"].find_one({"username": username})
        # if user:
        #     return User(**user)
