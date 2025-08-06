from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet
import os

from ..db import get_session
from ..models import Note
from ..schemas import NoteCreate, NoteOut

router = APIRouter()
fernet = Fernet(os.getenv('SECRET_KEY').encode())


@router.post("/", response_model=NoteOut)
async def create_note(
    note: NoteCreate, session: AsyncSession = Depends(get_session)
):
    encrypted = fernet.encrypt(note.encrypted_content.encode()).decode()
<<<<<<< HEAD
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
=======
    expires_at = datetime.utcnow() + timedelta(hours=1)
>>>>>>> 33ccd5c757eb5105c2822fc26774877895ee8caf
    new_note = Note(encrypted_content=encrypted, expires_at=expires_at,
                    read_once=note.read_once)
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note


@router.get("/{note_id}")
async def get_note(
    note_id: UUID, session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(Note).where(Note.id == note_id))
    note = result.scalar_one_or_none()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=404, detail="Note expired")
    content = fernet.decrypt(note.encrypted_content.encode()).decode()
    if note.read_once:
        await session.delete(note)
        await session.commit()
    return {"content": content}
