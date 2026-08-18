from typing import List, Optional, Dict, Any
from app.services.bible.bible_version_service import BibleVersionService
from app.services.bible.book_service import BookService
from app.services.bible.verse_search_service import VerseSearchService
from app.services.bible.topic_service import TopicService
from app.services.bible.character_service import CharacterService
from app.services.bible.cross_reference_service import CrossReferenceService
from app.services.bible.reference_parser import ReferenceParser
from app.models.domain import BibleVerse

class BibleService:
    def __init__(
        self,
        version_service: BibleVersionService,
        book_service: BookService,
        verse_search_service: VerseSearchService,
        topic_service: TopicService,
        character_service: CharacterService,
        cross_reference_service: CrossReferenceService
    ):
        self.version_service = version_service
        self.book_service = book_service
        self.verse_search_service = verse_search_service
        self.topic_service = topic_service
        self.character_service = character_service
        self.cross_reference_service = cross_reference_service

    def resolve_reference(self, reference: str, translation_code: str = "KJV") -> List[BibleVerse]:
        """Resolves a natural language reference into a list of verses."""
        parsed = ReferenceParser.parse(reference)
        if not parsed:
            return []
            
        import logging
        try:
            translation = self.version_service.get_translation_by_code(translation_code)
            if not translation:
                translations = self.version_service.translation_repo.get_all()
                if not translations:
                    logging.warning(f"Translation {translation_code} not found and no fallbacks available.")
                    return []
                translation = translations[0]
                logging.info(f"Translation {translation_code} not found. Falling back to {translation.code}.")
                
            book = self.book_service.get_book_by_name(parsed.book, str(translation.id))
            if not book:
                return []
                
            if not parsed.chapter:
                # Return entire book? For now, we only support chapter or verses.
                # Returning empty to signify unsupported large query.
                return []
                
            chapter = self.book_service.get_chapter(str(book.id), parsed.chapter)
            if not chapter:
                return []
                
            if not parsed.start_verse:
                verses = self.verse_search_service.get_verse_range(str(chapter.id), 1, 999)
            else:
                end_verse = parsed.end_verse if parsed.end_verse else parsed.start_verse
                verses = self.verse_search_service.get_verse_range(str(chapter.id), parsed.start_verse, end_verse)
                
            return verses
        except Exception as e:
            logging.warning(f"Failed to resolve reference {reference}: {e}")
            return []

    def search(self, query: str, translation_code: str = "KJV", book_id: Optional[str] = None, chapter_id: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[BibleVerse]:
        import logging
        try:
            translation = self.version_service.get_translation_by_code(translation_code)
            if not translation:
                translations = self.version_service.translation_repo.get_all()
                if not translations:
                    return []
                translation = translations[0]
            verses = self.verse_search_service.search(query, str(translation.id), book_id, chapter_id, limit, offset)
            return verses
        except Exception as e:
            logging.warning(f"Failed to search {query}: {e}")
            return []

    def get_daily_verse(self, translation_code: str = "KJV") -> Optional[BibleVerse]:
        from datetime import datetime
        import logging
        
        try:
            # Try to use the requested translation, but fallback to whatever exists if missing
            translation = self.version_service.get_translation_by_code(translation_code)
            if not translation:
                translations = self.version_service.translation_repo.get_all()
                if not translations:
                    return None
                translation = translations[0]
                translation_code = translation.code
            
            # A list of well-known verses to rotate through daily
            daily_verses = [
                "John 3:16", "Jeremiah 29:11", "Philippians 4:13", "Romans 8:28",
                "Proverbs 3:5", "Isaiah 41:10", "Psalm 46:1", "Galatians 5:22",
                "Hebrews 11:1", "2 Timothy 1:7", "1 Corinthians 13:4", "Matthew 11:28",
                "Romans 12:2", "Philippians 4:6", "Joshua 1:9", "Isaiah 40:31",
                "Ephesians 2:8", "Proverbs 3:6", "Romans 15:13", "Psalm 23:1"
            ]
            
            # Deterministically select verse based on day of year
            day_of_year = datetime.now().timetuple().tm_yday
            index = day_of_year % len(daily_verses)
            reference = daily_verses[index]
            
            verses = self.resolve_reference(reference, translation_code)
            if verses:
                return verses[0]
                        
            return None
        except Exception as e:
            logging.warning(f"Failed to get daily verse: {e}")
            return None
