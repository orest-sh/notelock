import motor.motor_asyncio
from odmantic import AIOEngine

from app.core.settings import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
engine = AIOEngine(client, database="notelock")
