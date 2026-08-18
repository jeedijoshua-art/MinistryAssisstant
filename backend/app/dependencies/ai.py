from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.repositories.conversation_repository import ConversationRepository, MessageRepository
from app.services.gemini_service import GeminiService
from app.services.prompt_service import PromptService
from app.services.memory_service import MemoryService
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService
from app.services.ai_service import AIService
from app.api.routers.bible import get_bible_service

def get_gemini_service() -> GeminiService:
    return GeminiService()

def get_prompt_service() -> PromptService:
    return PromptService()

def get_memory_service() -> MemoryService:
    return MemoryService()

def get_ai_service(
    db: Session = Depends(get_db),
    gemini_service: GeminiService = Depends(get_gemini_service),
    prompt_service: PromptService = Depends(get_prompt_service),
    memory_service: MemoryService = Depends(get_memory_service),
    bible_service = Depends(get_bible_service)
) -> AIService:
    from app.services.creative.creative_service import CreativeService
    from app.services.creative.brand_service import BrandService
    from app.services.creative.prompt_builder import PromptBuilderService
    from app.services.creative.pollinations_service import PollinationsService

    brand_service = BrandService(db)
    prompt_builder = PromptBuilderService(gemini_service)
    pollinations_service = PollinationsService()
    creative_service = CreativeService(db, brand_service, prompt_builder, pollinations_service)
    conversation_repo = ConversationRepository(db)
    message_repo = MessageRepository(db)
    
    chat_service = ChatService(
        conversation_repo=conversation_repo,
        message_repo=message_repo,
        gemini_service=gemini_service,
        prompt_service=prompt_service,
        memory_service=memory_service,
        bible_service=bible_service,
        creative_service=creative_service
    )
    conversation_service = ConversationService(conversation_repo)
    
    return AIService(chat_service=chat_service, conversation_service=conversation_service)
