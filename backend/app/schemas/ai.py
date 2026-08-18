from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class MessageSchema(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationCreate(BaseModel):
    church_id: Optional[UUID] = None
    title: Optional[str] = "New Conversation"

class ConversationUpdate(BaseModel):
    title: str

class ConversationResponse(BaseModel):
    id: UUID
    church_id: UUID
    title: str
    status: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageSchema] = []

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    conversation_id: UUID
    message: str
