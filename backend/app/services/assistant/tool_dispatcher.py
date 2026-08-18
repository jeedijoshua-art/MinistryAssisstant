from typing import List, Dict, Optional, Tuple, Any
import json
from pydantic import BaseModel, Field
from app.services.assistant.gemini_client import GeminiClient
from app.services.assistant.tools.base_tool import BaseTool
from app.services.assistant.tools.bible_tool import BibleTool
from app.services.assistant.tools.mock_tools import get_sermon_tool, get_prayer_tool, get_devotional_tool, get_poster_tool

class BibleToolArgs(BaseModel):
    query: str = Field(..., description="The reference or search term")
    is_search: bool = Field(..., description="True if searching for keywords, False if looking up a specific verse reference")
    translation: str = Field(..., description="The translation code, e.g. KJV")

class ToolDispatcher:
    def __init__(self, gemini_client, bible_tool, sermon_tool, prayer_tool, devotional_tool, poster_tool, writing_tool):
        self.gemini_client = gemini_client
        self.tools = {
            "BIBLE_QUERY": bible_tool,
            "SERMON_PREP": sermon_tool,
            "PRAYER_GEN": prayer_tool,
            "DEVOTIONAL_GEN": devotional_tool,
            "POSTER_GEN": poster_tool,
            "MINISTRY_WRITING": writing_tool
        }

    def dispatch(self, intent: str, recent_messages: List[Dict[str, str]], user_query: str = "", current_sermon_id: Optional[str] = None) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
        if intent not in self.tools or intent == "GENERAL_CHAT":
            return None, None
            
        tool = self.tools[intent]
        
        # Tools that require context
        if intent in ["SERMON_PREP", "PRAYER_GEN", "DEVOTIONAL_GEN", "POSTER_GEN", "MINISTRY_WRITING"]:
            # Pass history and context to these tools
            kwargs = {"user_query": user_query, "history": recent_messages}
            if current_sermon_id and intent in ["POSTER_GEN", "MINISTRY_WRITING"]:
                kwargs["sermon_id"] = current_sermon_id
                
            result = tool.execute(**kwargs)
            return result, {"tool_name": tool.name, "tool_args": kwargs}
            
        # For Bible Query, extract arguments
        if intent == "BIBLE_QUERY":
            extract_prompt = "You are a tool argument extractor. Extract the Bible reference or search query from the user's request."
            try:
                args_json = self.gemini_client.generate_content(
                    messages=recent_messages[-3:],
                    system_prompt=extract_prompt,
                    response_schema=BibleToolArgs
                )
                
                args_dict = json.loads(args_json)
                query = args_dict.get("query", "")
                is_search = args_dict.get("is_search", False)
                translation = args_dict.get("translation", "KJV")
                
                tool_result = tool.execute(query=query, is_search=is_search, translation=translation, user_query=user_query)
                
                return tool_result, {
                    "tool_name": tool.name,
                    "tool_args": {"query": query, "is_search": is_search, "translation": translation}
                }
                
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Tool dispatcher argument extraction failed: {e}")
                return None, None
                
        return None, None

