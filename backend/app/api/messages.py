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
from datetime import datetime, timezone
from app.api.trips_cache import save_trip_to_cache
from app.crud.trip import create_trip


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

    new_message = ChatMessage(
        session_id=session.id,
        role=data.role,
        content=data.content,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_message)
    await db.commit()

    # Trigger travel planner (example)
    try:
        trip_plan = create_trip(data.content, datetime.now(), "Munich Trip")
        await save_trip_to_cache(data.session_id, trip_plan)
        # await save_trip_to_db(data.session_id, trip_plan)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}



@router.get("/messages/{session_id}", response_model=List[ChatMessageRead])
async def get_messages(session_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(ChatMessage).where(ChatMessage.session_id == session_id)
    )
    messages = result.scalars().all()
    return jsonable_encoder(messages)
