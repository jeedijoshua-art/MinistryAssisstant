from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.services.sermon_service import SermonService
from app.services.sermon_ai_service import SermonAIService
from app.services.gemini_service import GeminiService
from app.services.bible.bible_service import BibleService
from app.schemas.sermon import SermonResponse, SermonCreate, SermonUpdate, SermonGenerateRequest, SermonAssistRequest
from app.dependencies.ai import get_gemini_service, get_bible_service
from app.config import get_settings
from app.core.limiter import limiter

router = APIRouter(prefix="/sermons", tags=["Sermons"])

def get_sermon_service(db: Session = Depends(get_db)) -> SermonService:
    return SermonService(db)

def get_sermon_ai_service(
    gemini: GeminiService = Depends(get_gemini_service),
    bible: BibleService = Depends(get_bible_service)
) -> SermonAIService:
    return SermonAIService(gemini, bible)

@router.get("", response_model=List[SermonResponse])
def get_sermons(limit: int = 50, offset: int = 0, svc: SermonService = Depends(get_sermon_service)):
    return svc.get_sermons(limit=limit, offset=offset)

@router.post("", response_model=SermonResponse)
def create_sermon(data: SermonCreate, svc: SermonService = Depends(get_sermon_service)):
    return svc.create_sermon(data.model_dump())

@router.get("/{sermon_id}", response_model=SermonResponse)
def get_sermon(sermon_id: UUID, svc: SermonService = Depends(get_sermon_service)):
    sermon = svc.get_sermon(sermon_id)
    if not sermon:
        raise HTTPException(status_code=404, detail="Sermon not found")
    return sermon

@router.put("/{sermon_id}", response_model=SermonResponse)
def update_sermon(sermon_id: UUID, data: SermonUpdate, svc: SermonService = Depends(get_sermon_service)):
    sermon = svc.update_sermon(sermon_id, data.model_dump(exclude_unset=True))
    if not sermon:
        raise HTTPException(status_code=404, detail="Sermon not found")
    return sermon

@router.delete("/{sermon_id}")
def delete_sermon(sermon_id: UUID, svc: SermonService = Depends(get_sermon_service)):
    if not svc.delete_sermon(sermon_id):
        raise HTTPException(status_code=404, detail="Sermon not found")
    return {"status": "ok"}

@router.post("/generate")
@limiter.limit("5/minute")
async def generate_sermon(req: SermonGenerateRequest, request: Request, svc: SermonAIService = Depends(get_sermon_ai_service)):
    return StreamingResponse(
        svc.generate_sermon_stream(req.model_dump()), 
        media_type="text/event-stream"
    )

@router.post("/assist")
@limiter.limit("20/minute")
async def assist_sermon(req: SermonAssistRequest, request: Request, svc: SermonAIService = Depends(get_sermon_ai_service)):
    return StreamingResponse(
        svc.assist_sermon_stream(req.action, req.current_content, req.selection),
        media_type="text/event-stream"
    )

@router.get("/{sermon_id}/export/docx")
def export_docx(sermon_id: UUID, svc: SermonService = Depends(get_sermon_service)):
    try:
        path = svc.export_sermon_docx(sermon_id)
        return FileResponse(path, filename=f"sermon_{sermon_id}.docx")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
