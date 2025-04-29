from app.db import engine
from app.models import chat, trip
from sqlalchemy.ext.asyncio import AsyncEngine

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(chat.Base.metadata.create_all)
        await conn.run_sync(trip.Base.metadata.create_all)

