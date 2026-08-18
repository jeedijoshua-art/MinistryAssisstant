from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class BrandProfileBase(BaseModel):
    logo_url: Optional[str] = None
    primary_color: str = "#0f172a"
    secondary_color: str = "#3b82f6"
    accent_color: str = "#eab308"
    heading_font: str = "Inter"
    body_font: str = "Inter"
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    social_handles: Dict[str, Any] = {}
    church_motto: Optional[str] = None

class BrandProfileResponse(BrandProfileBase):
    id: UUID
    church_id: UUID
    
    class Config:
        from_attributes = True

class BrandProfileUpdate(BrandProfileBase):
    pass

class CreativeAssetBase(BaseModel):
    id: UUID
    project_id: Optional[UUID] = None
    title: str
    asset_type: str
    url: str
    metadata_: Dict[str, Any] = {}

    class Config:
        from_attributes = True

class CreativeProjectBase(BaseModel):
    title: str
    media_type: str
    target_dimensions: Dict[str, Any] = {}
    editor_state: Dict[str, Any] = {}
    status: str = "draft"
    ai_prompt: Optional[str] = None

class CreativeProjectResponse(CreativeProjectBase):
    id: UUID
    sermon_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    assets: List[CreativeAssetBase] = []

    class Config:
        from_attributes = True

class CreativeProjectCreateFromSermon(BaseModel):
    sermon_id: UUID
    media_type: str

class CreativeProjectUpdate(BaseModel):
    title: Optional[str] = None
    editor_state: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
