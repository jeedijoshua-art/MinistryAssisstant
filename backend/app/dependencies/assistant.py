from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.assistant.gemini_client import GeminiClient
from app.services.assistant.conversation_manager import ConversationManager
from app.services.assistant.intent_detector import IntentDetector
from app.services.assistant.tool_dispatcher import ToolDispatcher
from app.services.assistant.assistant_service import AssistantService
from app.services.assistant.tools.bible_tool import BibleTool
from app.api.routers.bible import get_bible_service

def get_gemini_client() -> GeminiClient:
    return GeminiClient()

def get_conversation_manager(db: Session = Depends(get_db)) -> ConversationManager:
    return ConversationManager(db)

def get_intent_detector(gemini_client: GeminiClient = Depends(get_gemini_client)) -> IntentDetector:
    return IntentDetector(gemini_client)

from app.services.assistant.tools.sermon_tool import SermonTool
from app.services.assistant.tools.prayer_tool import PrayerTool
from app.services.assistant.tools.devotional_tool import DevotionalTool
from app.services.assistant.tools.ministry_writing_tool import MinistryWritingTool
from app.services.assistant.tools.creative_tool import CreativeStudioTool
from app.services.sermon_service import SermonService
from app.services.assistant.content_service import ContentService
from app.api.routers.sermon import get_sermon_service

def get_content_service(db: Session = Depends(get_db)) -> ContentService:
    return ContentService(db)

def get_tool_dispatcher(
    gemini_client: GeminiClient = Depends(get_gemini_client),
    bible_service = Depends(get_bible_service),
    sermon_service: SermonService = Depends(get_sermon_service),
    content_service: ContentService = Depends(get_content_service)
) -> ToolDispatcher:
    bible_tool = BibleTool(bible_service, gemini_client)
    sermon_tool = SermonTool(gemini_client, sermon_service)
    prayer_tool = PrayerTool(gemini_client, content_service)
    devotional_tool = DevotionalTool(gemini_client, content_service)
    poster_tool = CreativeStudioTool(gemini_client, content_service, bible_service)
    writing_tool = MinistryWritingTool(gemini_client, content_service)
    
    return ToolDispatcher(
        gemini_client, 
        bible_tool, 
        sermon_tool, 
        prayer_tool, 
        devotional_tool, 
        poster_tool, 
        writing_tool
    )

def get_assistant_service(
    gemini_client: GeminiClient = Depends(get_gemini_client),
    conversation_manager: ConversationManager = Depends(get_conversation_manager),
    intent_detector: IntentDetector = Depends(get_intent_detector),
    tool_dispatcher: ToolDispatcher = Depends(get_tool_dispatcher)
) -> AssistantService:
    return AssistantService(
        gemini_client=gemini_client,
        conversation_manager=conversation_manager,
        intent_detector=intent_detector,
        tool_dispatcher=tool_dispatcher
    )
