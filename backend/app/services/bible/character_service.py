from typing import List, Optional
from app.repositories.bible_repository import BibleCharacterRepository
from app.models.domain import BibleCharacter, BibleVerse

class CharacterService:
    def __init__(self, character_repo: BibleCharacterRepository):
        self.character_repo = character_repo
        
    def get_character_by_name(self, name: str) -> Optional[BibleCharacter]:
        return self.character_repo.get_by_name(name)
        
    def get_verses_for_character(self, character_id: str) -> List[BibleVerse]:
        return self.character_repo.get_verses_for_character(character_id)
