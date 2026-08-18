from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, AliasChoices

class MessageBase(BaseModel):
    role: str = Field(..., description="Role of the message author: 'user', 'assistant', 'system'")
    content: str = Field(..., description="Text content of the message")
    metadata_: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        validation_alias=AliasChoices("metadata_", "metadata"),
        serialization_alias="metadata"
    )

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: UUID
    conversation_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True

class ConversationBase(BaseModel):
    title: Optional[str] = "Untitled conversation"
    status: Optional[str] = "active"
    metadata_: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        validation_alias=AliasChoices("metadata_", "metadata"),
        serialization_alias="metadata"
    )

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    metadata_: Optional[Dict[str, Any]] = Field(
        None, 
        validation_alias=AliasChoices("metadata_", "metadata"),
        serialization_alias="metadata"
    )

class ConversationResponse(ConversationBase):
    id: UUID
    church_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True

class ConversationWithMessagesResponse(ConversationResponse):
    messages: List[MessageResponse] = []
