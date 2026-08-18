from typing import List, Optional
from app.repositories.bible_repository import BibleTranslationRepository
from app.models.domain import BibleTranslation

class BibleVersionService:
    def __init__(self, translation_repo: BibleTranslationRepository):
        self.translation_repo = translation_repo
        
    def get_all_translations(self) -> List[BibleTranslation]:
        # For a full implementation, you'd add this to the repo
        stmt = self.translation_repo.session.query(BibleTranslation).all()
        return stmt

    def get_translation_by_code(self, code: str) -> Optional[BibleTranslation]:
        return self.translation_repo.get_by_code(code)
