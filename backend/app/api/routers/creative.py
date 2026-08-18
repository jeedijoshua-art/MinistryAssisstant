from typing import List, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.session import get_db
from app.models.domain import GeneratedImage
from app.services.creative.creative_service import CreativeService
from app.services.creative.pollinations_service import PollinationsService
from pydantic import BaseModel

router = APIRouter(prefix="/creative", tags=["Creative Studio"])

class GenerateRequest(BaseModel):
    prompt: str
    conversation_id: UUID | None = None

def get_creative_service(db: Session = Depends(get_db)) -> CreativeService:
    pollinations = PollinationsService()
    return CreativeService(db, pollinations)

@router.post("/generate")
async def generate_image(req: GenerateRequest, creative_service: CreativeService = Depends(get_creative_service)):
    url = await creative_service.generate_project_media(
        prompt=req.prompt, 
        conversation_id=req.conversation_id, 
        tool_name="api_generate"
    )
    return {"status": "success", "url": url}

@router.get("/gallery")
def get_gallery(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    images = db.query(GeneratedImage).order_by(desc(GeneratedImage.created_at)).offset(offset).limit(limit).all()
    # Simple serialization
    return [
        {
            "id": str(img.id),
            "prompt": img.prompt,
            "provider": img.provider,
            "provider_model": img.provider_model,
            "cloudinary_url": img.cloudinary_url,
            "generation_status": img.generation_status,
            "created_at": img.created_at.isoformat(),
            "conversation_id": str(img.conversation_id) if img.conversation_id else None
        } for img in images
    ]

@router.get("/gallery/{id}")
def get_gallery_image(id: UUID, db: Session = Depends(get_db)):
    img = db.query(GeneratedImage).filter(GeneratedImage.id == id).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return {
        "id": str(img.id),
        "prompt": img.prompt,
        "provider": img.provider,
        "provider_model": img.provider_model,
        "cloudinary_url": img.cloudinary_url,
        "generation_status": img.generation_status,
        "created_at": img.created_at.isoformat(),
        "conversation_id": str(img.conversation_id) if img.conversation_id else None
    }

@router.delete("/gallery/{id}")
def delete_gallery_image(id: UUID, db: Session = Depends(get_db)):
    img = db.query(GeneratedImage).filter(GeneratedImage.id == id).first()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Note: We aren't deleting the Cloudinary image in this implementation, just the DB record.
    db.delete(img)
    db.commit()
    return {"status": "deleted"}
