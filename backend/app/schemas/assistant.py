from typing import Optional, List, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field
from app.schemas.conversation import MessageResponse

class AssistantChatRequest(BaseModel):
    message: str = Field(..., description="The user's input message.")
    conversation_id: Optional[UUID] = Field(None, description="The ID of an existing conversation to continue.")
    stream: bool = Field(False, description="Whether to stream the response.")

class ToolCallInfo(BaseModel):
    tool_name: str
    tool_args: Dict[str, Any]

class AssistantChatResponse(BaseModel):
    conversation_id: UUID
    message: MessageResponse
    tool_calls: Optional[List[ToolCallInfo]] = []
