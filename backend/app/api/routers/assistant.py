from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from app.schemas.assistant import AssistantChatRequest, AssistantChatResponse
from app.dependencies.assistant import get_assistant_service
from app.services.assistant.assistant_service import AssistantService

router = APIRouter(prefix="/assistant", tags=["Assistant Core"])

@router.post("/chat", response_model=AssistantChatResponse)
def chat(req: AssistantChatRequest, service: AssistantService = Depends(get_assistant_service)):
    try:
        if req.stream:
            raise HTTPException(status_code=400, detail="Use /stream endpoint for streaming")
        return service.chat(req.message, req.conversation_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
def chat_stream(req: AssistantChatRequest, service: AssistantService = Depends(get_assistant_service)):
    try:
        return StreamingResponse(
            service.chat_stream(req.message, req.conversation_id),
            media_type="text/plain"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel
from uuid import UUID
from app.services.assistant.export_service import ExportService
from app.services.assistant.conversation_manager import ConversationManager
from app.dependencies.assistant import get_conversation_manager

class ExportRequest(BaseModel):
    conversation_id: UUID
    format: str = "markdown"

@router.post("/export")
def export_conversation(
    request: ExportRequest,
    conversation_manager: ConversationManager = Depends(get_conversation_manager)
):
    """
    Exports a conversation into Markdown, JSON, or Text.
    """
    history = conversation_manager.get_chat_history_for_llm(request.conversation_id)
    if not history:
        raise HTTPException(status_code=404, detail="Conversation not found or empty.")
        
    try:
        exported_content = ExportService.export_conversation(history, request.format)
        return {"format": request.format, "content": exported_content}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
