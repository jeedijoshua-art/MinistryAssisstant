from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.models.domain import Prayer, Devotional, Church

class ContentService:
    def __init__(self, db: Session):
        self.db = db
        
    def _get_default_church_id(self) -> UUID:
        church = self.db.query(Church).first()
        if not church:
            church = Church(id=uuid4(), name="Default ZTP Church")
            self.db.add(church)
            self.db.commit()
        return church.id

    def create_prayer(self, data: Dict[str, Any], church_id: Optional[UUID] = None) -> Prayer:
        if not church_id:
            church_id = self._get_default_church_id()
            
        prayer = Prayer(
            id=uuid4(),
            church_id=church_id,
            title=data.get("title", "Untitled Prayer"),
            category=data.get("category", "General"),
            bible_verse=data.get("bible_verse"),
            content=data.get("content", ""),
            closing=data.get("closing"),
            status="draft"
        )
        self.db.add(prayer)
        self.db.commit()
        self.db.refresh(prayer)
        return prayer

    def create_devotional(self, data: Dict[str, Any], church_id: Optional[UUID] = None) -> Devotional:
        if not church_id:
            church_id = self._get_default_church_id()
            
        devotional = Devotional(
            id=uuid4(),
            church_id=church_id,
            title=data.get("title", "Untitled Devotional"),
            main_verse=data.get("main_verse", ""),
            reflection=data.get("reflection", ""),
            life_application=data.get("life_application"),
            prayer=data.get("prayer"),
            challenge=data.get("challenge"),
            reading_time=data.get("reading_time"),
            status="draft"
        )
        self.db.add(devotional)
        self.db.commit()
        self.db.refresh(devotional)
        return devotional

    def create_creative_project(self, data: Dict[str, Any], sermon_id: Optional[UUID] = None) -> Any:
        from app.models.domain import CreativeProject
        project = CreativeProject(
            id=uuid4(),
            sermon_id=sermon_id,
            title=data.get("title", "Untitled Poster"),
            media_type="poster",
            status="draft",
            ai_prompt=data.get("image_prompt", ""),
            editor_state=data
        )
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def create_communication_project(self, data: Dict[str, Any], sermon_id: Optional[UUID] = None) -> Any:
        from app.models.domain import CommunicationProject, CommunicationAsset
        project = CommunicationProject(
            id=uuid4(),
            sermon_id=sermon_id,
            title=data.get("title", "Untitled Communication"),
            campaign_type=data.get("campaign_type", "General"),
            status="draft"
        )
        self.db.add(project)
        
        asset = CommunicationAsset(
            id=uuid4(),
            project_id=project.id,
            platform=data.get("platform", "Text"),
            content=data.get("content", ""),
            status="draft"
        )
        self.db.add(asset)
        
        self.db.commit()
        self.db.refresh(project)
        return project

