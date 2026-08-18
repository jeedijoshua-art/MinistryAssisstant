from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class SermonSectionBase(BaseModel):
    id: Optional[UUID] = None
    title: str
    content: str
    order_index: int

    class Config:
        from_attributes = True

class SermonBase(BaseModel):
    id: Optional[UUID] = None
    title: str
    theme: Optional[str] = None
    main_verse: Optional[str] = None
    bible_version: str = "KJV"
    audience: Optional[str] = None
    occasion: Optional[str] = None
    estimated_duration: Optional[int] = None
    date_preached: Optional[str] = None
    content: Optional[str] = None
    status: str = "draft"
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

class SermonResponse(SermonBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    sections: List[SermonSectionBase] = []

    class Config:
        from_attributes = True

class SermonCreate(BaseModel):
    title: str
    theme: Optional[str] = None
    main_verse: Optional[str] = None
    bible_version: str = "KJV"
    audience: Optional[str] = None
    occasion: Optional[str] = None
    estimated_duration: Optional[int] = None
    date_preached: Optional[str] = None
    content: Optional[str] = None
    status: str = "draft"
    notes: Optional[str] = None
    sections: List[SermonSectionBase] = []

class SermonUpdate(SermonCreate):
    pass

class SermonGenerateRequest(BaseModel):
    main_verse: str
    theme: Optional[str] = None
    audience: Optional[str] = None

class SermonAssistRequest(BaseModel):
    action: str
    current_content: str
    selection: Optional[str] = None
