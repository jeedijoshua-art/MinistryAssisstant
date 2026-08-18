from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from app.models.domain import Conversation, Message, Church

class ConversationManager:
    def __init__(self, db: Session):
        self.db = db

    def _get_default_church_id(self) -> UUID:
        """
        Temporary helper to get or create a default church if authentication doesn't provide one.
        In a real scenario, church_id should come from the current user context.
        """
        church = self.db.query(Church).first()
        if not church:
            church = Church(id=uuid4(), name="Default ZTP Church")
            self.db.add(church)
            self.db.commit()
        return church.id

    def create_conversation(self, title: str = "Untitled conversation", church_id: Optional[UUID] = None) -> Conversation:
        if not church_id:
            church_id = self._get_default_church_id()
            
        conv = Conversation(
            id=uuid4(),
            church_id=church_id,
            title=title,
            status="active",
            metadata_={}
        )
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv

    def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def get_user_conversations(self, church_id: UUID, limit: int = 50, offset: int = 0) -> List[Conversation]:
        return self.db.query(Conversation)\
            .filter(Conversation.church_id == church_id)\
            .order_by(Conversation.updated_at.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()

    def delete_conversation(self, conversation_id: UUID) -> bool:
        conv = self.get_conversation(conversation_id)
        if not conv:
            return False
        self.db.delete(conv)
        self.db.commit()
        return True

    def add_message(self, conversation_id: UUID, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> Message:
        if metadata is None:
            metadata = {}
            
        msg = Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata_=metadata
        )
        self.db.add(msg)
        self.db.flush()
        
        # Touch conversation updated_at
        conv = self.get_conversation(conversation_id)
        if conv:
            conv.updated_at = msg.created_at # Ensure update cascade happens or explicitly touch
            
        self.db.commit()
        self.db.refresh(msg)
        return msg

    def get_messages(self, conversation_id: UUID, limit: int = 100) -> List[Message]:
        return self.db.query(Message)\
            .filter(Message.conversation_id == conversation_id)\
            .order_by(Message.created_at.asc())\
            .limit(limit)\
            .all()
            
    def get_chat_history_for_llm(self, conversation_id: UUID, limit: int = 20) -> List[Dict[str, str]]:
        messages = self.get_messages(conversation_id, limit)
        history = []
        for msg in messages:
            # We don't send system messages injected with tool outputs as part of standard history
            # unless we format them specifically. But Gemini handles basic user/model roles best.
            history.append({
                "role": msg.role,
                "content": msg.content
            })
        return history
