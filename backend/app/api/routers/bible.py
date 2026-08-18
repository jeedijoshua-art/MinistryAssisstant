from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.schemas.bible import BibleBookBase, BibleChapterBase, BibleVerseBase, BibleTopicBase, BibleCharacterBase, CrossReferenceBase, BibleTranslationBase
from app.repositories.bible_repository import (
    BibleBookRepository, BibleChapterRepository, BibleVerseRepository, 
    BibleTopicRepository, BibleCharacterRepository, CrossReferenceRepository, BibleTranslationRepository
)
from app.services.bible.bible_version_service import BibleVersionService
from app.services.bible.book_service import BookService
from app.services.bible.verse_search_service import VerseSearchService
from app.services.bible.topic_service import TopicService
from app.services.bible.character_service import CharacterService
from app.services.bible.cross_reference_service import CrossReferenceService
from app.services.bible.bible_service import BibleService
from app.services.bible.import_service import BibleImportService

router = APIRouter(prefix="/bible", tags=["Bible"])

def get_bible_service(db: Session = Depends(get_db)) -> BibleService:
    version_service = BibleVersionService(BibleTranslationRepository(db))
    book_service = BookService(BibleBookRepository(db), BibleChapterRepository(db))
    verse_search_service = VerseSearchService(BibleVerseRepository(db))
    topic_service = TopicService(BibleTopicRepository(db))
    character_service = CharacterService(BibleCharacterRepository(db))
    cross_reference_service = CrossReferenceService(CrossReferenceRepository(db))
    
    return BibleService(
        version_service, book_service, verse_search_service, 
        topic_service, character_service, cross_reference_service
    )

@router.get("/books", response_model=List[BibleBookBase])
def get_books(translation_code: str = "KJV", svc: BibleService = Depends(get_bible_service)):
    translation = svc.version_service.get_translation_by_code(translation_code)
    if not translation:
        translations = svc.version_service.translation_repo.get_all()
        if not translations:
            raise HTTPException(status_code=404, detail="Translation not found and no fallbacks available")
        translation = translations[0]
    return svc.book_service.get_books(str(translation.id))

@router.get("/book/{book_id}", response_model=BibleBookBase)
def get_book(book_id: str, svc: BibleService = Depends(get_bible_service)):
    book = svc.book_service.book_repo.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/chapter/{chapter_id}", response_model=BibleChapterBase)
def get_chapter(chapter_id: str, svc: BibleService = Depends(get_bible_service)):
    chapter = svc.book_service.chapter_repo.get(chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@router.get("/daily-verse", response_model=BibleVerseBase)
def get_daily_verse(translation_code: str = "KJV", svc: BibleService = Depends(get_bible_service)):
    verse = svc.get_daily_verse(translation_code)
    if not verse:
        raise HTTPException(status_code=404, detail="Daily verse not found")
    return verse

@router.get("/verse", response_model=List[BibleVerseBase])
def resolve_verse(reference: str, translation_code: str = "KJV", svc: BibleService = Depends(get_bible_service)):
    verses = svc.resolve_reference(reference, translation_code)
    if not verses:
        raise HTTPException(status_code=404, detail="Reference not found or unsupported.")
    return verses

@router.get("/search", response_model=List[BibleVerseBase])
def search(
    query: str, 
    translation_code: str = "KJV", 
    book_id: Optional[str] = None, 
    chapter_id: Optional[str] = None, 
    limit: int = 20, 
    offset: int = 0, 
    svc: BibleService = Depends(get_bible_service)
):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")
    return svc.search(query, translation_code, book_id, chapter_id, limit, offset)

@router.get("/topics", response_model=List[BibleTopicBase])
def search_topics(query: str, svc: BibleService = Depends(get_bible_service)):
    return svc.topic_service.search_topics(query)

@router.get("/topic/{topic_id}", response_model=BibleTopicBase)
def get_topic(topic_id: str, svc: BibleService = Depends(get_bible_service)):
    topic = svc.topic_service.topic_repo.get(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.get("/character/{character_id}", response_model=BibleCharacterBase)
def get_character(character_id: str, svc: BibleService = Depends(get_bible_service)):
    char = svc.character_service.character_repo.get(character_id)
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")
    return char

@router.get("/compare", response_model=dict)
def compare_verse(reference: str, translations: str = "KJV,NIV", svc: BibleService = Depends(get_bible_service)):
    codes = translations.split(",")
    results = {}
    for code in codes:
        results[code] = svc.resolve_reference(reference, code.strip())
    return results

@router.get("/cross-reference/{verse_id}", response_model=List[CrossReferenceBase])
def get_cross_references(verse_id: str, svc: BibleService = Depends(get_bible_service)):
    return svc.cross_reference_service.get_cross_references(verse_id)

@router.get("/translations", response_model=List[BibleTranslationBase])
def get_translations(svc: BibleService = Depends(get_bible_service)):
    return svc.version_service.get_all_translations()

@router.get("/translation/{translation_id}", response_model=BibleTranslationBase)
def get_translation(translation_id: str, svc: BibleService = Depends(get_bible_service)):
    translation = svc.version_service.translation_repo.get(translation_id)
    if not translation:
        raise HTTPException(status_code=404, detail="Translation not found")
    return translation

@router.post("/translation/import")
async def import_translation(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are supported for import")
    content = await file.read()
    try:
        import_svc = BibleImportService(db)
        stats = import_svc.import_json(content.decode("utf-8"))
        return {"message": "Import successful", "stats": stats}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

@router.get("/chapters/{book_id}", response_model=List[BibleChapterBase])
def get_chapters(book_id: str, svc: BibleService = Depends(get_bible_service)):
    return svc.book_service.get_chapters(book_id)
