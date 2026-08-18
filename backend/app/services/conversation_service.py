import logging
from uuid import UUID, uuid4
from app.models.domain import Conversation
from app.repositories.conversation_repository import ConversationRepository

class ConversationService:
    def __init__(self, conversation_repo: ConversationRepository):
        self.conversation_repo = conversation_repo

    def create(self, church_id: UUID | None, title: str | None = None) -> Conversation:
        if not title:
            title = "New Conversation"
        
        actual_church_id = church_id if church_id else uuid4()
        conv = Conversation(church_id=actual_church_id, title=title)
        
        try:
            # Need to commit to actually hit the DB errors now if the repo uses flush or commit
            # Using repo add will attempt to save it. If the transaction rolls back, we catch it.
            res = self.conversation_repo.add(conv)
            self.conversation_repo.session.commit()
            return res
        except Exception as e:
            self.conversation_repo.session.rollback()
            logging.warning(f"Failed to save conversation to DB, using in-memory fallback: {e}")
            conv.id = uuid4()
            return conv

    def get(self, conversation_id: UUID) -> Conversation | None:
        try:
            return self.conversation_repo.get(conversation_id)
        except Exception as e:
            logging.warning(f"Failed to get conversation from DB: {e}")
            return None

    def list_all(self, church_id: UUID):
        try:
            return self.conversation_repo.list_all(church_id)
        except Exception as e:
            logging.warning(f"Failed to list conversations from DB: {e}")
            return []

    def delete(self, conversation_id: UUID) -> bool:
        try:
            res = self.conversation_repo.delete_conversation(conversation_id)
            self.conversation_repo.session.commit()
            return res
        except Exception as e:
            self.conversation_repo.session.rollback()
            logging.warning(f"Failed to delete conversation: {e}")
            return False
    
    def update(self, conversation_id: UUID, title: str) -> Conversation | None:
        try:
            conv = self.conversation_repo.get(conversation_id)
            if conv:
                conv.title = title
                self.conversation_repo.session.commit()
            return conv
        except Exception as e:
            self.conversation_repo.session.rollback()
            logging.warning(f"Failed to update conversation: {e}")
            return None
