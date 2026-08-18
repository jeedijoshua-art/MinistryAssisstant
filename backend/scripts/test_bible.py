import logging
from app.database.session import SessionLocal
from app.repositories.bible_repository import BibleVerseRepository
from app.services.bible.bible_service import BibleService
from app.services.bible.bible_version_service import BibleVersionService
from app.repositories.bible_repository import BibleTranslationRepository
from app.services.bible.book_service import BookService
from app.repositories.bible_repository import BibleBookRepository, BibleChapterRepository
from app.services.bible.verse_search_service import VerseSearchService
from app.services.bible.topic_service import TopicService
from app.repositories.bible_repository import BibleTopicRepository
from app.services.bible.character_service import CharacterService
from app.repositories.bible_repository import BibleCharacterRepository
from app.services.bible.cross_reference_service import CrossReferenceService
from app.repositories.bible_repository import CrossReferenceRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    db = SessionLocal()
    try:
        version_service = BibleVersionService(BibleTranslationRepository(db))
        book_service = BookService(BibleBookRepository(db), BibleChapterRepository(db))
        verse_search_service = VerseSearchService(BibleVerseRepository(db))
        topic_service = TopicService(BibleTopicRepository(db))
        character_service = CharacterService(BibleCharacterRepository(db))
        cross_reference_service = CrossReferenceService(CrossReferenceRepository(db))
        
        svc = BibleService(
            version_service, book_service, verse_search_service, 
            topic_service, character_service, cross_reference_service
        )

        logger.info("Testing resolve_reference('Genesis 1:1')")
        # Find translation to use
        translations = version_service.get_all_translations()
        if not translations:
            logger.error("No translations found in database!")
            return
        
        code = translations[0].code
        logger.info(f"Using translation: {code}")
        
        verses = svc.resolve_reference("Genesis 1:1", translation_code=code)
        for v in verses:
            logger.info(f"Found: {v.chapter.book.name} {v.chapter.chapter_number}:{v.verse_number} - {v.text}")
            
        logger.info("Testing search_verses('faith love')")
        results = svc.search("faith love", translation_code=code)
        logger.info(f"Found {len(results)} verses containing 'faith' and 'love'")
        
        logger.info("Testing search_verses('\"faith love\"')")
        results = svc.search('"faith love"', translation_code=code)
        logger.info(f"Found {len(results)} exact phrase matches")

    except Exception as e:
        logger.error(f"Error during testing: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
