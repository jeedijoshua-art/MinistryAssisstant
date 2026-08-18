from typing import List, Optional
from app.repositories.bible_repository import BibleVerseRepository
from app.models.domain import BibleVerse

class VerseSearchService:
    def __init__(self, verse_repo: BibleVerseRepository):
        self.verse_repo = verse_repo
        
    def get_verse(self, chapter_id: str, verse_number: int) -> Optional[BibleVerse]:
        return self.verse_repo.get_verse(chapter_id, verse_number)
        
    def get_verse_range(self, chapter_id: str, start: int, end: int) -> List[BibleVerse]:
        return self.verse_repo.get_verses_in_range(chapter_id, start, end)
        
    def search(self, query: str, translation_id: str, book_id: Optional[str] = None, chapter_id: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[BibleVerse]:
        return self.verse_repo.search_verses(query, translation_id, book_id, chapter_id, limit, offset)
