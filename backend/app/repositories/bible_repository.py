from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.repositories.base import Repository
from app.models.domain import (
    BibleTranslation, BibleBook, BibleChapter, BibleVerse, 
    CrossReference, BibleTopic, BibleCharacter, TopicVerse, CharacterReference
)

class BibleTranslationRepository(Repository[BibleTranslation]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, BibleTranslation)
        
    def get_by_code(self, code: str) -> Optional[BibleTranslation]:
        stmt = select(BibleTranslation).where(BibleTranslation.code == code)
        return self.session.execute(stmt).scalars().first()

    def get_all(self) -> List[BibleTranslation]:
        stmt = select(BibleTranslation)
        return list(self.session.execute(stmt).scalars().all())
        
class BibleBookRepository(Repository[BibleBook]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, BibleBook)
        
    def get_by_name(self, name: str, translation_id: str) -> Optional[BibleBook]:
        stmt = select(BibleBook).where(
            BibleBook.name.ilike(name), 
            BibleBook.translation_id == translation_id
        )
        return self.session.execute(stmt).scalars().first()

    def get_all_books(self, translation_id: str) -> List[BibleBook]:
        stmt = select(BibleBook).where(BibleBook.translation_id == translation_id).order_by(BibleBook.book_number)
        return list(self.session.execute(stmt).scalars().all())

class BibleChapterRepository(Repository[BibleChapter]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, BibleChapter)
        
    def get_by_book_and_number(self, book_id: str, number: int) -> Optional[BibleChapter]:
        stmt = select(BibleChapter).where(
            BibleChapter.book_id == book_id,
            BibleChapter.chapter_number == number
        )
        return self.session.execute(stmt).scalars().first()

    def get_chapters_for_book(self, book_id: str) -> List[BibleChapter]:
        stmt = select(BibleChapter).where(BibleChapter.book_id == book_id).order_by(BibleChapter.chapter_number)
        return list(self.session.execute(stmt).scalars().all())

class BibleVerseRepository(Repository[BibleVerse]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, BibleVerse)
        
    def get_verse(self, chapter_id: str, verse_number: int) -> Optional[BibleVerse]:
        stmt = select(BibleVerse).options(
            joinedload(BibleVerse.chapter).joinedload(BibleChapter.book)
        ).where(
            BibleVerse.chapter_id == chapter_id,
            BibleVerse.verse_number == verse_number
        )
        return self.session.execute(stmt).scalars().first()

    def get_verses_in_range(self, chapter_id: str, start: int, end: int) -> List[BibleVerse]:
        stmt = select(BibleVerse).options(
            joinedload(BibleVerse.chapter).joinedload(BibleChapter.book)
        ).where(
            BibleVerse.chapter_id == chapter_id,
            BibleVerse.verse_number >= start,
            BibleVerse.verse_number <= end
        ).order_by(BibleVerse.verse_number)
        return list(self.session.execute(stmt).scalars().all())
        
    def search_verses(self, query: str, translation_id: str, book_id: Optional[str] = None, chapter_id: Optional[str] = None, limit: int = 20, offset: int = 0) -> List[BibleVerse]:
        from sqlalchemy import and_
        stmt = (
            select(BibleVerse)
            .join(BibleChapter).join(BibleBook)
            .options(joinedload(BibleVerse.chapter).joinedload(BibleChapter.book))
        )
        
        conditions = [BibleBook.translation_id == translation_id]
        if book_id:
            conditions.append(BibleBook.id == book_id)
        if chapter_id:
            conditions.append(BibleChapter.id == chapter_id)
            
        query = query.strip()
        if query.startswith('"') and query.endswith('"'):
            exact_phrase = query.strip('"')
            conditions.append(BibleVerse.text.ilike(f"%{exact_phrase}%"))
        else:
            words = query.split()
            for word in words:
                conditions.append(BibleVerse.text.ilike(f"%{word}%"))
                
        stmt = stmt.where(and_(*conditions)).limit(limit).offset(offset)
        return list(self.session.execute(stmt).scalars().all())

class CrossReferenceRepository(Repository[CrossReference]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, CrossReference)
        
    def get_for_verse(self, verse_id: str) -> List[CrossReference]:
        stmt = select(CrossReference).where(CrossReference.from_verse_id == verse_id)
        return list(self.session.execute(stmt).scalars().all())

class BibleTopicRepository(Repository[BibleTopic]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, BibleTopic)
        
    def get_by_name(self, name: str) -> Optional[BibleTopic]:
        stmt = select(BibleTopic).where(BibleTopic.name.ilike(name))
        return self.session.execute(stmt).scalars().first()
        
    def search(self, query: str) -> List[BibleTopic]:
        stmt = select(BibleTopic).where(BibleTopic.name.ilike(f"%{query}%"))
        return list(self.session.execute(stmt).scalars().all())

    def get_verses_for_topic(self, topic_id: str) -> List[BibleVerse]:
        stmt = (
            select(BibleVerse)
            .join(TopicVerse, TopicVerse.verse_id == BibleVerse.id)
            .where(TopicVerse.topic_id == topic_id)
        )
        return list(self.session.execute(stmt).scalars().all())

class BibleCharacterRepository(Repository[BibleCharacter]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, BibleCharacter)
        
    def get_by_name(self, name: str) -> Optional[BibleCharacter]:
        stmt = select(BibleCharacter).where(BibleCharacter.name.ilike(name))
        return self.session.execute(stmt).scalars().first()

    def get_verses_for_character(self, character_id: str) -> List[BibleVerse]:
        stmt = (
            select(BibleVerse)
            .join(CharacterReference, CharacterReference.verse_id == BibleVerse.id)
            .where(CharacterReference.character_id == character_id)
        )
        return list(self.session.execute(stmt).scalars().all())
