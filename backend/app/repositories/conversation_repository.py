from typing import Sequence
from uuid import UUID
from sqlalchemy import select
from app.repositories.base import Repository
from app.models.domain import Conversation, Message

class ConversationRepository(Repository[Conversation]):
    def __init__(self, session):
        super().__init__(session, Conversation)

    def list_all(self, church_id: UUID) -> Sequence[Conversation]:
        stmt = select(Conversation).where(Conversation.church_id == church_id).order_by(Conversation.created_at.desc())
        return self.session.execute(stmt).scalars().all()

    def get_with_messages(self, conversation_id: UUID) -> Conversation | None:
        # Simple get, can be optimized with joinedload if needed
        return self.get(conversation_id)

    def delete_conversation(self, conversation_id: UUID) -> bool:
        conv = self.get(conversation_id)
        if conv:
            self.session.delete(conv)
            self.session.flush()
            return True
        return False

class MessageRepository(Repository[Message]):
    def __init__(self, session):
        super().__init__(session, Message)

    def list_by_conversation(self, conversation_id: UUID) -> Sequence[Message]:
        stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
        return self.session.execute(stmt).scalars().all()
