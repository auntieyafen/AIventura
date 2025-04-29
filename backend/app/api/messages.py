from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from pydantic import BaseModel
from app.db import get_session
from app.models.chat import ChatMessage
from app.crud.chat import get_or_create_chat_session
from datetime import datetime, timezone, timedelta
from app.api.trips_cache import save_trip_to_cache
from app.crud.trip import create_trip
from app.agents.trip_planner_autogen import create_trip_plan

router = APIRouter()

class ChatMessageCreate(BaseModel):
    session_id: UUID
    role: str
    content: str

class ChatMessageRead(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/messages")
async def post_message(data: ChatMessageCreate, db: AsyncSession = Depends(get_session)):
    session = await get_or_create_chat_session(data.session_id, db)

    # Save user message
    new_message = ChatMessage(
        session_id=session.id,
        role=data.role,
        content=data.content,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_message)
    await db.commit()

    try:
        # Step 1: Run travel planner
        start_date = datetime.now()
        trip_plan = create_trip_plan(data.content, start_date, "AI Trip")

        # Step 2: Estimate end_date based on number of days
        end_date = start_date + timedelta(days=len(trip_plan.get("days", [])))

        # Step 3: Save to DB and cache
        await create_trip(
            db=db,
            session_id=data.session_id,
            start_date=start_date,
            end_date=datetime.now().date() + timedelta(days=2),
            trip_name="Munich Trip",
            trip_data=trip_plan
        )
        await save_trip_to_cache(data.session_id, trip_plan)

        # Step 4: Return to frontend
        return {"status": "ok", "trip": trip_plan}
    
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@router.get("/messages/{session_id}", response_model=List[ChatMessageRead])
async def get_messages(session_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(ChatMessage).where(ChatMessage.session_id == session_id)
    )
    messages = result.scalars().all()
    return jsonable_encoder(messages)
