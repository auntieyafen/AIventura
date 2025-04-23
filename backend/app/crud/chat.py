from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime
from app.models.chat import ChatSession
from sqlalchemy.ext.asyncio import AsyncSession

async def get_or_create_chat_session(session_id: UUID, db: AsyncSession) -> ChatSession:
    existing = await db.execute(select(ChatSession).where(ChatSession.id == session_id))
    session = existing.scalar_one_or_none()
    if session:
        return session
    new_session = ChatSession(id=session_id, created_at=datetime.utcnow())
    db.add(new_session)
    await db.commit()
    return new_session
