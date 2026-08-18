from typing import List, Dict
from pydantic import BaseModel, Field
from app.services.assistant.gemini_client import GeminiClient
from app.services.assistant.prompts import INTENT_SYSTEM_PROMPT

class IntentResponse(BaseModel):
    intent: str = Field(..., description="The classified intent, e.g. BIBLE_QUERY, SERMON_PREP, GENERAL_CHAT, etc.")

class IntentDetector:
    def __init__(self, gemini_client: GeminiClient):
        self.gemini_client = gemini_client

    def detect_intent(self, recent_messages: List[Dict[str, str]]) -> str:
        """
        Takes the recent conversation history and uses Gemini 
        with structured output to classify the user's intent.
        """
        # Ensure we only send the last few messages for intent classification to save tokens
        messages_to_send = recent_messages[-5:] if len(recent_messages) > 5 else recent_messages
        
        try:
            # We use the generate_content with a response_schema to force structured output
            response_text = self.gemini_client.generate_content(
                messages=messages_to_send,
                system_prompt=INTENT_SYSTEM_PROMPT,
                response_schema=IntentResponse
            )
            
            import json
            try:
                # The response should be a JSON string matching IntentResponse schema
                data = json.loads(response_text)
                return data.get("intent", "GENERAL_CHAT")
            except Exception:
                # Fallback if the model didn't return valid JSON
                if "BIBLE" in response_text.upper():
                    return "BIBLE_QUERY"
                elif "SERMON" in response_text.upper():
                    return "SERMON_PREP"
                elif "PRAYER" in response_text.upper():
                    return "PRAYER_GEN"
                elif "WRITE" in response_text.upper() or "ANNOUNCEMENT" in response_text.upper():
                    return "MINISTRY_WRITING"
                return "GENERAL_CHAT"
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Intent detection failed: {e}")
            return "GENERAL_CHAT"
