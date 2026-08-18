from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field

class DesignType(str, Enum):
    VERSE = "verse"
    SERVICE = "service"
    BIBLE_STUDY = "bible_study"
    PRAYER_MEETING = "prayer_meeting"
    YOUTH_EVENT = "youth_event"
    ANNOUNCEMENT = "announcement"
    CONFERENCE = "conference"
    BANNER = "banner"
    EMBLEM = "emblem"
    SOCIAL_MEDIA = "social_media"
    PRINT = "print"
    GENERAL = "general"

class Orientation(str, Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"
    SQUARE = "square"

class TextElement(BaseModel):
    text: str
    font_size_multiplier: float = 1.0
    color: str = "#FFFFFF"
    
class DesignSpec(BaseModel):
    design_type: DesignType
    orientation: Orientation
    width: int
    height: int
    
    visual_theme: str = Field(..., description="Semantic theme for the artwork (e.g., 'creation', 'peaceful landscape', 'storm').")
    visual_prompt: str = Field(..., description="Highly detailed visual prompt for Pollinations. MUST explicitly instruct to NOT generate text.")
    
    # Text content
    primary_text: Optional[str] = None
    secondary_text: Optional[str] = None
    supporting_text: Optional[str] = None
    
    # Event specific
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    
    # Bible specific
    has_bible_reference: bool = False
    bible_reference: Optional[str] = None
    translation: Optional[str] = "KJV"
    
    # Branding
    church_name: Optional[str] = None
    tagline: Optional[str] = None
    emblem_required: bool = False
    
    # Generated during composition
    actual_verse_text: Optional[str] = None
    full_reference: Optional[str] = None
