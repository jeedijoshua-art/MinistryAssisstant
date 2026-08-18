from typing import List
from app.repositories.bible_repository import CrossReferenceRepository
from app.models.domain import CrossReference

class CrossReferenceService:
    def __init__(self, cross_ref_repo: CrossReferenceRepository):
        self.cross_ref_repo = cross_ref_repo
        
    def get_cross_references(self, verse_id: str) -> List[CrossReference]:
        return self.cross_ref_repo.get_for_verse(verse_id)
