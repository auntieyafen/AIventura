import json
from typing import Optional
from uuid import UUID

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.trip import Trip

# If using Cloud Redis, change the redis://localhost:6379
redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)


async def save_trip_to_cache(session_id: UUID, trip_data: dict, ttl_seconds: int = 3600) -> None:
    await redis_client.set(f"trip:{session_id}", json.dumps(trip_data), ex=ttl_seconds)


async def get_trip_from_cache(session_id: UUID) -> Optional[dict]:
    trip_str = await redis_client.get(f"trip:{session_id}")
    if trip_str:
        return json.loads(trip_str)
    return None


async def delete_trip_from_cache(session_id: UUID) -> None:
    await redis_client.delete(f"trip:{session_id}")


# ------------ fallback DB ------------

async def get_trip(session_id: UUID, db: AsyncSession) -> Optional[dict]:
    trip_data = await get_trip_from_cache(session_id)
    if trip_data is not None:
        return trip_data

    result = await db.execute(select(Trip).where(Trip.session_id == session_id))
    trip = result.scalar_one_or_none()

    if trip is not None:
        trip_dict = {
            "id": str(trip.id),
            "session_id": str(trip.session_id),
            "start_date": trip.start_date.isoformat() if trip.start_date else None,
            "end_date": trip.end_date.isoformat() if trip.end_date else None,
            "trip_name": trip.trip_name,
            "trip_data": trip.trip_data,
        }
        await save_trip_to_cache(session_id, trip_dict)
        return trip_dict

    return None
