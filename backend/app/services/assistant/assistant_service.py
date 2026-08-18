from typing import Optional, List, Dict, Any, Generator
from uuid import UUID
from app.services.assistant.gemini_client import GeminiClient
from app.services.assistant.conversation_manager import ConversationManager
from app.services.assistant.intent_detector import IntentDetector
from app.services.assistant.tool_dispatcher import ToolDispatcher
from app.services.assistant.response_formatter import ResponseFormatter
from app.services.assistant.prompts import SYSTEM_PROMPT
from app.schemas.assistant import AssistantChatResponse, ToolCallInfo
from app.schemas.conversation import MessageResponse

class AssistantService:
    def __init__(
        self,
        gemini_client: GeminiClient,
        conversation_manager: ConversationManager,
        intent_detector: IntentDetector,
        tool_dispatcher: ToolDispatcher
    ):
        self.gemini_client = gemini_client
        self.conversation_manager = conversation_manager
        self.intent_detector = intent_detector
        self.tool_dispatcher = tool_dispatcher

    def _process_message(self, message: str, conversation_id: Optional[UUID] = None) -> tuple[UUID, List[Dict[str, str]], List[ToolCallInfo]]:
        # Ensure conversation exists
        if not conversation_id:
            conv = self.conversation_manager.create_conversation(title=message[:50] + "...")
            conversation_id = conv.id
        else:
            conv = self.conversation_manager.get_conversation(conversation_id)
            if not conv:
                raise ValueError("Conversation not found")

        # Save user message
        self.conversation_manager.add_message(conversation_id, role="user", content=message)
        
        # Get chat history
        history = self.conversation_manager.get_chat_history_for_llm(conversation_id)
        
        # Detect Intent
        intent = self.intent_detector.detect_intent(history)
        
        # Dispatch Tool (if applicable)
        current_sermon_id = conv.metadata_.get("current_sermon_id") if conv.metadata_ else None
        tool_output, tool_info = self.tool_dispatcher.dispatch(
            intent=intent, 
            recent_messages=history, 
            user_query=message, 
            current_sermon_id=current_sermon_id
        )
        
        tool_calls = []
        if tool_output and tool_info:
            tool_calls.append(ToolCallInfo(**tool_info))
            # Format context and replace the last user message with the injected one
            formatted_prompt = ResponseFormatter.format_user_prompt_with_context(message, ResponseFormatter.format_tool_context(tool_info['tool_name'], tool_output))
            # We override the last message in history before sending to Gemini
            history[-1]["content"] = formatted_prompt
            
        return conversation_id, history, tool_calls

    def chat(self, message: str, conversation_id: Optional[UUID] = None) -> AssistantChatResponse:
        """
        Synchronous chat response.
        """
        conv_id, history, tool_calls = self._process_message(message, conversation_id)
        
        # Call Gemini
        response_text = self.gemini_client.generate_content(
            messages=history,
            system_prompt=SYSTEM_PROMPT
        )
        
        # Save assistant message
        msg = self.conversation_manager.add_message(
            conversation_id=conv_id,
            role="assistant",
            content=response_text,
            metadata={"tool_calls": [tc.dict() for tc in tool_calls]} if tool_calls else {}
        )
        
        return AssistantChatResponse(
            conversation_id=conv_id,
            message=MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                metadata=msg.metadata_,
                created_at=msg.created_at,
                updated_at=msg.updated_at
            ),
            tool_calls=tool_calls
        )

    def chat_stream(self, message: str, conversation_id: Optional[UUID] = None) -> Generator[str, None, None]:
        """
        Streaming chat response.
        Yields chunks of text and saves the final message to the database once finished.
        """
        conv_id, history, tool_calls = self._process_message(message, conversation_id)
        
        full_response = ""
        stream = self.gemini_client.generate_content_stream(
            messages=history,
            system_prompt=SYSTEM_PROMPT
        )
        
        # Optionally stream tool context note first to inform UI
        if tool_calls:
            yield f"\n*[Using internal tool: {tool_calls[0].tool_name}]*\n\n"
            
        for chunk in stream:
            full_response += chunk
            yield chunk
            
        # Save assistant message after streaming completes
        self.conversation_manager.add_message(
            conversation_id=conv_id,
            role="assistant",
            content=full_response,
            metadata={"tool_calls": [tc.dict() for tc in tool_calls]} if tool_calls else {}
        )
