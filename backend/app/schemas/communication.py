from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class CommunicationAssetBase(BaseModel):
    id: UUID
    project_id: Optional[UUID] = None
    platform: str
    content_length: str
    content: Optional[str] = None
    status: str

    class Config:
        from_attributes = True

class CommunicationProjectBase(BaseModel):
    title: str
    campaign_type: str
    status: str = "draft"

class CommunicationProjectResponse(CommunicationProjectBase):
    id: UUID
    sermon_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    assets: List[CommunicationAssetBase] = []

    class Config:
        from_attributes = True

class CommunicationGenerateRequest(BaseModel):
    sermon_id: UUID

class CommunicationAssetUpdate(BaseModel):
    content: str
