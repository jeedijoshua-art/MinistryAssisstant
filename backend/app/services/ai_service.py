from uuid import UUID
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService

class AIService:
    """
    Façade for all AI operations. Combines chat orchestration and conversation management.
    """
    def __init__(self, chat_service: ChatService, conversation_service: ConversationService):
        self.chat_service = chat_service
        self.conversation_service = conversation_service

    # Expose necessary methods for the routers
    def create_conversation(self, church_id: UUID, title: str | None = None):
        return self.conversation_service.create(church_id, title)
    
    def get_conversation(self, conversation_id: UUID):
        return self.conversation_service.get(conversation_id)

    def list_conversations(self, church_id: UUID):
        return self.conversation_service.list_all(church_id)

    def delete_conversation(self, conversation_id: UUID):
        return self.conversation_service.delete(conversation_id)
    
    def update_conversation(self, conversation_id: UUID, title: str):
        return self.conversation_service.update(conversation_id, title)

    def stream_chat(self, conversation_id: UUID, message: str):
        # We can also add rate-limiting checks or token tracking here using AIUsageRepo
        return self.chat_service.stream_conversation(conversation_id, message)
