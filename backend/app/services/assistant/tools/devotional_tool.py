import json
from pydantic import BaseModel, Field
from app.services.assistant.tools.base_tool import BaseTool
from app.services.assistant.gemini_client import GeminiClient
from app.services.assistant.content_service import ContentService
from app.services.assistant.prompts.devotional_prompts import DEVOTIONAL_TOOL_SYSTEM_PROMPT
from typing import List, Dict

class DevotionalOutput(BaseModel):
    title: str = Field(..., description="The title of the devotional")
    main_verse: str = Field(..., description="The scripture text and reference")
    reflection: str = Field(..., description="The reflection content")
    life_application: str = Field(..., description="The application steps")
    prayer: str = Field(..., description="A short prayer")
    challenge: str = Field(..., description="A challenge for the day")
    reading_time: int = Field(..., description="Estimated reading time in minutes")
    markdown_content: str = Field(..., description="The complete formatted markdown string combining all the elements")

class DevotionalTool(BaseTool):
    def __init__(self, gemini_client: GeminiClient, content_service: ContentService):
        self.gemini_client = gemini_client
        self.content_service = content_service
        
    @property
    def name(self) -> str:
        return "devotional_tool"
        
    @property
    def description(self) -> str:
        return "Generates complete devotionals based on user requests."
        
    def execute(self, user_query: str, history: List[Dict[str, str]], **kwargs) -> str:
        try:
            response_json = self.gemini_client.generate_content(
                messages=history + [{"role": "user", "content": user_query}],
                system_prompt=DEVOTIONAL_TOOL_SYSTEM_PROMPT,
                response_schema=DevotionalOutput
            )
            
            data = json.loads(response_json)
            
            # Persist to database
            devotional = self.content_service.create_devotional({
                "title": data.get("title", "Untitled Devotional"),
                "main_verse": data.get("main_verse", ""),
                "reflection": data.get("reflection", ""),
                "life_application": data.get("life_application", ""),
                "prayer": data.get("prayer", ""),
                "challenge": data.get("challenge", ""),
                "reading_time": data.get("reading_time", 3)
            })
            
            return f"Devotional '{devotional.title}' created successfully (ID: {devotional.id}).\n\nPreview:\n{data.get('markdown_content', '')}"
            
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Devotional Tool error: {e}")
            return f"Failed to generate devotional: {str(e)}"
