from schemas.user import User
from utils.hashing import get_password_hash
import asyncio
from configs.database import init


async def run_seed():
    await init()
    users = [
        User(fullname="Root",
             username="admin",
             disabled=False,
             hashed_password=get_password_hash('admin')
             ),
        User(fullname="Softrebel",
             username="softrebel",
             disabled=False,
             hashed_password=get_password_hash('123456')
             ),
    ]

    # bulk_operator = [
    #     UpdateOne(
    #         {'pk': item['username']},
    #         {'$setOnInsert': item},
    #         upsert=True
    #     ) for item in users
    # ]
    # await db.user.bulk_write(bulk_operator)
    await User.insert_many(users)
asyncio.run(run_seed())
