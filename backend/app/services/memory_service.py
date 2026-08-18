from app.models.domain import Conversation

class MemoryService:
    def __init__(self):
        pass

    def get_context(self, conversation: Conversation) -> str:
        """
        Extracts preferences and historical topics from conversation metadata
        to augment the system prompt or context window.
        """
        meta = conversation.metadata_ or {}
        preferred_version = meta.get("preferred_version", "KJV")
        topics = meta.get("recent_topics", [])
        
        context_str = f"User preferred Bible version: {preferred_version}.\n"
        if topics:
            context_str += f"Recent topics discussed: {', '.join(topics)}.\n"
            
        return context_str

    def update_memory(self, conversation: Conversation, new_metadata: dict):
        """
        Updates the conversation's memory (metadata).
        """
        current = conversation.metadata_ or {}
        current.update(new_metadata)
        conversation.metadata_ = current
