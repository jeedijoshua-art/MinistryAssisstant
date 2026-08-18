import logging
from app.database.session import SessionLocal
from app.dependencies.assistant import (
    get_gemini_client,
    get_conversation_manager,
    get_intent_detector,
    get_tool_dispatcher,
    get_assistant_service
)
from app.services.bible.bible_version_service import BibleVersionService
from app.repositories.bible_repository import BibleTranslationRepository
from app.services.bible.book_service import BookService
from app.repositories.bible_repository import BibleBookRepository, BibleChapterRepository
from app.services.bible.verse_search_service import VerseSearchService
from app.repositories.bible_repository import BibleVerseRepository
from app.services.bible.topic_service import TopicService
from app.repositories.bible_repository import BibleTopicRepository
from app.services.bible.character_service import CharacterService
from app.repositories.bible_repository import BibleCharacterRepository
from app.services.bible.cross_reference_service import CrossReferenceService
from app.repositories.bible_repository import CrossReferenceRepository
from app.services.bible.bible_service import BibleService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    db = SessionLocal()
    try:
        # Manually assemble BibleService
        version_service = BibleVersionService(BibleTranslationRepository(db))
        book_service = BookService(BibleBookRepository(db), BibleChapterRepository(db))
        verse_search_service = VerseSearchService(BibleVerseRepository(db))
        topic_service = TopicService(BibleTopicRepository(db))
        character_service = CharacterService(BibleCharacterRepository(db))
        cross_reference_service = CrossReferenceService(CrossReferenceRepository(db))
        
        bible_service = BibleService(
            version_service, book_service, verse_search_service, 
            topic_service, character_service, cross_reference_service
        )
        
        from app.services.sermon_service import SermonService
        from app.services.assistant.content_service import ContentService
        
        sermon_service = SermonService(db)
        content_service = ContentService(db)
        
        # Assemble Assistant Service
        gemini_client = get_gemini_client()
        conv_manager = get_conversation_manager(db)
        intent_detector = get_intent_detector(gemini_client)
        tool_dispatcher = get_tool_dispatcher(gemini_client, bible_service, sermon_service, content_service)
        
        assistant = get_assistant_service(gemini_client, conv_manager, intent_detector, tool_dispatcher)
        
        logger.info("=== Testing General Chat Intent ===")
        res = assistant.chat("Hello! Who are you?")
        logger.info(f"Response: {res.message.content}")
        
        logger.info("=== Testing Bible Query Intent ===")
        res2 = assistant.chat("Can you explain Genesis 1:1 to me?", conversation_id=res.conversation_id)
        logger.info(f"Response: {res2.message.content}")
        logger.info(f"Tool Calls: {res2.tool_calls}")

        logger.info("=== Testing Poster Gen (Mock Phase 4) ===")
        res3 = assistant.chat("Generate a poster for Sunday Service", conversation_id=res.conversation_id)
        logger.info(f"Response: {res3.message.content}")
        logger.info(f"Tool Calls: {res3.tool_calls}")

    except Exception as e:
        logger.error(f"Error during testing: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
