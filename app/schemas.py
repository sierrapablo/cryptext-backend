from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class NoteCreate(BaseModel):
    encrypted_content: str
    read_once: bool = False


class NoteOut(NoteCreate):
    id: UUID
    created_at: datetime
