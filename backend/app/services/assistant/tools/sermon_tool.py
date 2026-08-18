import json
from pydantic import BaseModel, Field
from app.services.assistant.tools.base_tool import BaseTool
from app.services.assistant.gemini_client import GeminiClient
from app.services.sermon_service import SermonService
from app.services.assistant.prompts.sermon_prompts import SERMON_TOOL_SYSTEM_PROMPT
from typing import List, Dict

class SermonOutput(BaseModel):
    title: str = Field(..., description="The title of the sermon")
    theme: str = Field(..., description="The main theme of the sermon")
    main_scripture: str = Field(..., description="The primary scripture reference")
    markdown_content: str = Field(..., description="The full markdown formatted sermon content")

class SermonTool(BaseTool):
    def __init__(self, gemini_client: GeminiClient, sermon_service: SermonService):
        self.gemini_client = gemini_client
        self.sermon_service = sermon_service
        
    @property
    def name(self) -> str:
        return "sermon_tool"
        
    @property
    def description(self) -> str:
        return "Generates complete sermons based on user requests."
        
    def execute(self, user_query: str, history: List[Dict[str, str]], **kwargs) -> str:
        try:
            # We enforce a JSON schema to ensure we extract the title and theme correctly
            response_json = self.gemini_client.generate_content(
                messages=history + [{"role": "user", "content": user_query}],
                system_prompt=SERMON_TOOL_SYSTEM_PROMPT,
                response_schema=SermonOutput
            )
            
            data = json.loads(response_json)
            title = data.get("title", "Untitled Sermon")
            theme = data.get("theme", "")
            main_scripture = data.get("main_scripture", "")
            content = data.get("markdown_content", "")
            
            # Persist to database
            sermon = self.sermon_service.create_sermon({
                "title": title,
                "theme": theme,
                "main_verse": main_scripture,
                "content": content,
                "status": "draft"
            })
            
            # The tool output gets injected into context, so the assistant can say "I've created the sermon..."
            return f"Sermon '{title}' created successfully and saved with ID: {sermon.id}.\n\nPreview:\n{content}"
            
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Sermon Tool error: {e}")
            return f"Failed to generate sermon: {str(e)}"
