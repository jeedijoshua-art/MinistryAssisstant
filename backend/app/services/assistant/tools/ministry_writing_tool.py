import json
from uuid import UUID
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from app.services.assistant.tools.base_tool import BaseTool
from app.services.assistant.gemini_client import GeminiClient
from app.services.assistant.content_service import ContentService
from app.services.assistant.prompts.ministry_writing_prompts import MINISTRY_WRITING_SYSTEM_PROMPT

class MinistryWritingOutput(BaseModel):
    title: str = Field(..., description="Title of the communication")
    platform: str = Field(..., description="E.g., WhatsApp, Email, Instagram")
    campaign_type: str = Field(..., description="E.g., Announcement, Invitation")
    content: str = Field(..., description="The main message content")
    markdown_content: str = Field(..., description="The formatted preview to show the user")

class MinistryWritingTool(BaseTool):
    def __init__(self, gemini_client: GeminiClient, content_service: ContentService):
        self.gemini_client = gemini_client
        self.content_service = content_service
        
    @property
    def name(self) -> str:
        return "ministry_writing_tool"
        
    @property
    def description(self) -> str:
        return "Generates church announcements and ministry communications."
        
    def execute(self, user_query: str, history: List[Dict[str, str]], sermon_id: Optional[UUID] = None, **kwargs) -> str:
        try:
            response_json = self.gemini_client.generate_content(
                messages=history + [{"role": "user", "content": user_query}],
                system_prompt=MINISTRY_WRITING_SYSTEM_PROMPT,
                response_schema=MinistryWritingOutput
            )
            
            data = json.loads(response_json)
            
            # Persist to database
            project = self.content_service.create_communication_project({
                "title": data.get("title", "Untitled Comm"),
                "platform": data.get("platform", "Text"),
                "campaign_type": data.get("campaign_type", "General"),
                "content": data.get("content", "")
            }, sermon_id=sermon_id)
            
            return f"Communication '{project.title}' drafted successfully (ID: {project.id}).\n\n{data.get('markdown_content')}"
            
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Ministry Writing Tool error: {e}")
            return f"Failed to generate communication: {str(e)}"
