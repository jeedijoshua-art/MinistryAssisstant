from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Dict, Any, Optional
from app.models.domain import BrandProfile

class BrandService:
    def __init__(self, db: Session):
        self.db = db

    def get_brand_profile(self, church_id: UUID) -> Optional[BrandProfile]:
        import logging
        try:
            query = select(BrandProfile).where(BrandProfile.church_id == church_id)
            result = self.db.execute(query).scalar_one_or_none()
        except Exception as e:
            logging.warning(f"Failed to query brand profile: {e}")
            result = None
        
        # Auto-initialize if not exists for the church
        if not result:
            result = BrandProfile(
                id=uuid4(),
                church_id=church_id,
                primary_color="#0f172a",
                secondary_color="#3b82f6",
                accent_color="#eab308",
                heading_font="Inter",
                body_font="Inter"
            )
            try:
                self.db.add(result)
                self.db.commit()
                self.db.refresh(result)
            except Exception as e:
                self.db.rollback()
                logging.warning(f"Failed to auto-init brand profile in DB: {e}")
            
        return result

    def update_brand_profile(self, church_id: UUID, data: Dict[str, Any]) -> BrandProfile:
        import logging
        profile = self.get_brand_profile(church_id)
        
        for key, value in data.items():
            if hasattr(profile, key) and key not in ["id", "church_id", "created_at", "updated_at"]:
                setattr(profile, key, value)
                
        try:
            self.db.commit()
            self.db.refresh(profile)
        except Exception as e:
            self.db.rollback()
            logging.warning(f"Failed to update brand profile in DB: {e}")
            
        return profile
