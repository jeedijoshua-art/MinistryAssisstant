from typing import List, Optional
from app.repositories.bible_repository import BibleBookRepository, BibleChapterRepository
from app.models.domain import BibleBook, BibleChapter

class BookService:
    def __init__(self, book_repo: BibleBookRepository, chapter_repo: BibleChapterRepository):
        self.book_repo = book_repo
        self.chapter_repo = chapter_repo
        
    def get_books(self, translation_id: str) -> List[BibleBook]:
        return self.book_repo.get_all_books(translation_id)
        
    def get_book_by_name(self, name: str, translation_id: str) -> Optional[BibleBook]:
        return self.book_repo.get_by_name(name, translation_id)
        
    def get_chapter(self, book_id: str, chapter_number: int) -> Optional[BibleChapter]:
        return self.chapter_repo.get_by_book_and_number(book_id, chapter_number)
        
    def get_chapters(self, book_id: str) -> List[BibleChapter]:
        return self.chapter_repo.get_chapters_for_book(book_id)
