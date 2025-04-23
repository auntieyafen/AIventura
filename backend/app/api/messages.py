from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID
from pydantic import BaseModel
from app.db import get_session
from app.models.chat import ChatMessage
from app.crud.chat import get_or_create_chat_session

router = APIRouter()

class ChatMessageCreate(BaseModel):
    session_id: UUID
    role: str
    content: str

async def create_message(data: ChatMessageCreate, db: AsyncSession = Depends(get_session)):
    msg = ChatMessage(**data.model_dump())
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

@router.post("/messages")
async def post_message(data: ChatMessageCreate, db: AsyncSession = Depends(get_session)):
    session = await get_or_create_chat_session(data.session_id, db)
    
    new_message = ChatMessage(
        session_id=session.id,
        role=data.role,
        content=data.content,
    )
    db.add(new_message)
    await db.commit()
    return {"status": "ok"}

@router.get("/messages")
async def get_messages(session_id: UUID, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(ChatMessage).where(ChatMessage.session_id == session_id)
    )
    return result.scalars().all()
