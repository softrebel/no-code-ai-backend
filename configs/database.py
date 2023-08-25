import motor.motor_asyncio
from beanie import init_beanie
from schemas import File, User, Model
from .settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client.NoCodeAI


async def init():
    # Create Motor client
    # Initialize beanie with the Product document class and a database
    await init_beanie(database=db, document_models=[File, User, Model])
