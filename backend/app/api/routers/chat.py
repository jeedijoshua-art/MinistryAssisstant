from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from app.schemas.ai import ChatRequest
from app.dependencies.ai import get_ai_service
from app.services.ai_service import AIService
from app.core.limiter import limiter

router = APIRouter(prefix="/chat", tags=["AI Chat"])

@router.post("")
@limiter.limit("10/minute")
def chat_stream(req: ChatRequest, request: Request, ai_service: AIService = Depends(get_ai_service)):
    # Stream the generator response
    generator = ai_service.stream_chat(req.conversation_id, req.message)
    
    def sse_format():
        for chunk in generator:
            yield chunk

    # Return StreamingResponse. The frontend will consume this stream.
    return StreamingResponse(sse_format(), media_type="text/plain")
