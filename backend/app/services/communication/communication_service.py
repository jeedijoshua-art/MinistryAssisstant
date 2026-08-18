from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from typing import List, Dict, Any, Optional
import asyncio

from app.models.domain import CommunicationProject, CommunicationAsset, Sermon, BrandProfile
from app.services.creative.brand_service import BrandService
from app.services.communication.communication_ai_service import CommunicationAIService

class CommunicationService:
    def __init__(self, db: Session, brand_service: BrandService, ai_service: CommunicationAIService):
        self.db = db
        self.brand_service = brand_service
        self.ai_service = ai_service

    def get_projects(self, limit: int = 20, offset: int = 0) -> List[CommunicationProject]:
        query = select(CommunicationProject).order_by(desc(CommunicationProject.created_at))
        result = self.db.execute(query.limit(limit).offset(offset))
        return list(result.scalars().all())

    def get_project(self, project_id: UUID) -> Optional[CommunicationProject]:
        return self.db.get(CommunicationProject, project_id)
        
    def delete_project(self, project_id: UUID) -> bool:
        project = self.get_project(project_id)
        if project:
            self.db.delete(project)
            self.db.commit()
            return True
        return False

    async def generate_communications(self, sermon_id: UUID, church_id: UUID) -> CommunicationProject:
        sermon = self.db.get(Sermon, sermon_id)
        if not sermon:
            raise ValueError("Sermon not found")

        brand = self.brand_service.get_brand_profile(church_id)
        
        # Create Root Project
        project = CommunicationProject(
            id=uuid4(),
            sermon_id=sermon_id,
            title=f"Communications for {sermon.title}",
            campaign_type="Sermon Announcement Bundle",
            status="draft"
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        
        # Define platforms to generate
        platforms = [
            "Instagram Caption",
            "Facebook Caption",
            "WhatsApp Message",
            "Church Bulletin",
            "Email Newsletter"
        ]
        
        # Generate in parallel for speed
        tasks = []
        for platform in platforms:
            tasks.append(self._generate_and_save_asset(project.id, platform, sermon, brand))
            
        await asyncio.gather(*tasks)
        
        self.db.refresh(project)
        return project

    async def _generate_and_save_asset(self, project_id: UUID, platform: str, sermon: Sermon, brand: BrandProfile):
        content = await self.ai_service.generate_platform_asset(platform, sermon, brand)
        asset = CommunicationAsset(
            id=uuid4(),
            project_id=project_id,
            platform=platform,
            content=content,
            status="draft"
        )
        self.db.add(asset)
        self.db.commit()
        
    def update_asset(self, asset_id: UUID, content: str) -> Optional[CommunicationAsset]:
        asset = self.db.get(CommunicationAsset, asset_id)
        if asset:
            asset.content = content
            self.db.commit()
            self.db.refresh(asset)
        return asset
