from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class BibleVerseBase(BaseModel):
    id: UUID
    chapter_id: UUID
    verse_number: int
    text: str
    
    class Config:
        from_attributes = True

class BibleChapterBase(BaseModel):
    id: UUID
    book_id: UUID
    chapter_number: int
    
    class Config:
        from_attributes = True

class BibleBookBase(BaseModel):
    id: UUID
    translation_id: UUID
    name: str
    abbreviation: str
    testament: str
    book_number: int

    class Config:
        from_attributes = True

class BibleTranslationBase(BaseModel):
    id: UUID
    code: str
    name: str
    language: str

    class Config:
        from_attributes = True

class BibleTopicBase(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class BibleCharacterBase(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    biography: Optional[str] = None
    
    class Config:
        from_attributes = True

class CrossReferenceBase(BaseModel):
    id: UUID
    from_verse_id: UUID
    to_verse_id: UUID
    reference_type: str
    
    class Config:
        from_attributes = True
