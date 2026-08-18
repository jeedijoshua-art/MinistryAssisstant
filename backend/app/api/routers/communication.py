from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database.session import get_db
from app.services.creative.brand_service import BrandService
from app.services.communication.communication_service import CommunicationService
from app.services.communication.communication_ai_service import CommunicationAIService
from app.services.gemini_service import GeminiService
from app.dependencies.ai import get_gemini_service
from app.dependencies.auth import get_current_church_id
from app.schemas.communication import (
    CommunicationProjectResponse, CommunicationGenerateRequest, CommunicationAssetUpdate
)
from app.core.limiter import limiter

router = APIRouter(prefix="/communications", tags=["Communications Engine"])

def get_brand_service(db: Session = Depends(get_db)) -> BrandService:
    return BrandService(db)

def get_communication_service(
    db: Session = Depends(get_db),
    brand_service: BrandService = Depends(get_brand_service),
    gemini_service: GeminiService = Depends(get_gemini_service)
) -> CommunicationService:
    ai_service = CommunicationAIService(gemini_service)
    return CommunicationService(db, brand_service, ai_service)

@router.get("", response_model=List[CommunicationProjectResponse])
def get_projects(limit: int = 50, offset: int = 0, svc: CommunicationService = Depends(get_communication_service)):
    return svc.get_projects(limit=limit, offset=offset)

@router.get("/{project_id}", response_model=CommunicationProjectResponse)
def get_project(project_id: UUID, svc: CommunicationService = Depends(get_communication_service)):
    project = svc.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/generate", response_model=CommunicationProjectResponse)
@limiter.limit("5/minute")
async def generate_communications(
    data: CommunicationGenerateRequest,
    request: Request,
    church_id: UUID = Depends(get_current_church_id),
    svc: CommunicationService = Depends(get_communication_service)
):
    try:
        return await svc.generate_communications(data.sermon_id, church_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/assets/{asset_id}")
def update_asset(
    asset_id: UUID, 
    data: CommunicationAssetUpdate, 
    svc: CommunicationService = Depends(get_communication_service)
):
    asset = svc.update_asset(asset_id, data.content)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"status": "ok"}

@router.delete("/{project_id}")
def delete_project(project_id: UUID, svc: CommunicationService = Depends(get_communication_service)):
    if not svc.delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "ok"}
