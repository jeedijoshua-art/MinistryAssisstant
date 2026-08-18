from app.services.assistant.tools.base_tool import BaseTool
from app.services.bible.bible_service import BibleService
from app.services.assistant.gemini_client import GeminiClient
from app.services.assistant.prompts.bible_prompts import BIBLE_TOOL_SYSTEM_PROMPT
from typing import Optional, List, Dict

class BibleTool(BaseTool):
    def __init__(self, bible_service: BibleService, gemini_client: GeminiClient):
        self.bible_service = bible_service
        self.gemini_client = gemini_client
        
    @property
    def name(self) -> str:
        return "bible_tool"
        
    @property
    def description(self) -> str:
        return "Retrieves and explains Bible verses from the database."
        
    def execute(self, query: str, is_search: bool = False, translation: str = "KJV", user_query: str = "", **kwargs) -> str:
        try:
            db_context = ""
            if is_search:
                results = self.bible_service.search(query, translation_code=translation, limit=5)
                if not results:
                    db_context = f"No results found for '{query}' in {translation}."
                else:
                    for v in results:
                        db_context += f"- **{v.chapter.book.name} {v.chapter.chapter_number}:{v.verse_number}**: {v.text}\n"
            else:
                results = self.bible_service.resolve_reference(query, translation_code=translation)
                if not results:
                    db_context = f"Reference '{query}' not found in {translation}."
                else:
                    for v in results:
                        db_context += f"> {v.text} [{v.verse_number}]\n"
            
            # Now synthesize an explanation using Gemini
            messages = [{"role": "user", "content": f"User asked: {user_query}\n\nDatabase results:\n{db_context}"}]
            explanation = self.gemini_client.generate_content(
                messages=messages,
                system_prompt=BIBLE_TOOL_SYSTEM_PROMPT
            )
            return explanation
            
        except Exception as e:
            return f"Error retrieving Bible data: {e}"
