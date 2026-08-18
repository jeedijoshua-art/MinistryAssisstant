from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.schemas.conversation import ConversationCreate, ConversationUpdate, ConversationResponse, MessageResponse, ConversationWithMessagesResponse
from app.dependencies.assistant import get_conversation_manager
from app.services.assistant.conversation_manager import ConversationManager

router = APIRouter(prefix="/conversations", tags=["Conversations"])

@router.post("", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(req: ConversationCreate, manager: ConversationManager = Depends(get_conversation_manager)):
    # The manager defaults church_id if None
    conv = manager.create_conversation(title=req.title or "Untitled conversation")
    return conv

@router.get("/{id}", response_model=ConversationWithMessagesResponse)
def get_conversation(id: UUID, manager: ConversationManager = Depends(get_conversation_manager)):
    conv = manager.get_conversation(id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Optional: Attach messages to the response
    messages = manager.get_messages(id)
    conv_dict = {
        "id": conv.id,
        "church_id": conv.church_id,
        "title": conv.title,
        "status": conv.status,
        "metadata_": conv.metadata_,
        "created_at": conv.created_at,
        "updated_at": conv.updated_at,
        "messages": messages
    }
    return conv_dict

@router.get("", response_model=List[ConversationResponse])
def list_conversations(church_id: UUID, limit: int = 50, offset: int = 0, manager: ConversationManager = Depends(get_conversation_manager)):
    return manager.get_user_conversations(church_id, limit, offset)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(id: UUID, manager: ConversationManager = Depends(get_conversation_manager)):
    if not manager.delete_conversation(id):
        raise HTTPException(status_code=404, detail="Conversation not found")

@router.get("/{id}/messages", response_model=List[MessageResponse])
def get_messages(id: UUID, manager: ConversationManager = Depends(get_conversation_manager)):
    return manager.get_messages(id)
