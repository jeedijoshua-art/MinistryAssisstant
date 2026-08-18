import json
from pydantic import BaseModel, Field
from app.services.assistant.tools.base_tool import BaseTool
from app.services.assistant.gemini_client import GeminiClient
from app.services.assistant.content_service import ContentService
from app.services.assistant.prompts.prayer_prompts import PRAYER_TOOL_SYSTEM_PROMPT
from typing import List, Dict

class PrayerOutput(BaseModel):
    title: str = Field(..., description="The title of the prayer")
    category: str = Field(..., description="The category, e.g., Healing, Family")
    bible_verse: str = Field(..., description="A relevant Bible verse reference")
    content: str = Field(..., description="The main prayer content in markdown")
    closing: str = Field(..., description="The closing of the prayer")

class PrayerTool(BaseTool):
    def __init__(self, gemini_client: GeminiClient, content_service: ContentService):
        self.gemini_client = gemini_client
        self.content_service = content_service
        
    @property
    def name(self) -> str:
        return "prayer_tool"
        
    @property
    def description(self) -> str:
        return "Generates structured prayers based on user requests."
        
    def execute(self, user_query: str, history: List[Dict[str, str]], **kwargs) -> str:
        try:
            response_json = self.gemini_client.generate_content(
                messages=history + [{"role": "user", "content": user_query}],
                system_prompt=PRAYER_TOOL_SYSTEM_PROMPT,
                response_schema=PrayerOutput
            )
            
            data = json.loads(response_json)
            
            # Persist to database
            prayer = self.content_service.create_prayer({
                "title": data.get("title", "Untitled Prayer"),
                "category": data.get("category", "General"),
                "bible_verse": data.get("bible_verse", ""),
                "content": data.get("content", ""),
                "closing": data.get("closing", "")
            })
            
            return f"Prayer '{prayer.title}' generated successfully (ID: {prayer.id}).\n\n{prayer.content}\n\n**{prayer.closing}**"
            
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Prayer Tool error: {e}")
            return f"Failed to generate prayer: {str(e)}"
