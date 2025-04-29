from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.trip import Trip
from typing import Optional
from uuid import UUID

def serialize_trip(trip: Trip) -> dict:
    return {
        "id": str(trip.id),
        "session_id": str(trip.session_id),
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "trip_name": trip.trip_name,
        "trip_data": trip.trip_data,
    }

async def create_trip(
    db: AsyncSession,
    session_id: UUID,
    start_date: Optional[str],
    end_date: Optional[str],
    trip_name: Optional[str],
    trip_data: dict
) -> Trip:
    new_trip = Trip(
        session_id=session_id,
        start_date=start_date,
        end_date=end_date,
        trip_name=trip_name,
        trip_data=trip_data,
    )
    db.add(new_trip)
    await db.commit()
    await db.refresh(new_trip)
    return new_trip

async def get_trip_by_session_id(db: AsyncSession, session_id: UUID) -> Optional[Trip]:
    result = await db.execute(
        select(Trip).where(Trip.session_id == session_id)
    )
    trip = result.scalars().first()
    return trip

async def update_trip(
    db: AsyncSession,
    session_id: UUID,
    trip_data: dict
) -> Optional[Trip]:
    result = await db.execute(
        select(Trip).where(Trip.session_id == session_id)
    )
    trip = result.scalars().first()

    if trip:
        trip.trip_data = trip_data
        await db.commit()
        await db.refresh(trip)
    
    return trip

async def delete_trip(db: AsyncSession, session_id: UUID) -> bool:
    result = await db.execute(
        select(Trip).where(Trip.session_id == session_id)
    )
    trip = result.scalars().first()

    if trip:
        await db.delete(trip)
        await db.commit()
        return True
    return False
