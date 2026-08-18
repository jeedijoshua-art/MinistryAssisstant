from typing import AsyncGenerator, Dict, Any, Optional
from app.services.gemini_service import GeminiService
from app.services.bible.bible_service import BibleService

class SermonAIService:
    def __init__(self, gemini_service: GeminiService, bible_service: BibleService):
        self.gemini_service = gemini_service
        self.bible_service = bible_service

    async def generate_sermon_stream(self, data: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """
        Generates a structured sermon based on inputs.
        Retrieves context from Bible Engine FIRST.
        """
        main_verse = data.get("main_verse")
        theme = data.get("theme", "")
        audience = data.get("audience", "")
        
        # 1. Retrieve Bible Context
        bible_context = ""
        if main_verse:
            search_results = self.bible_service.verse_search_service.search_verses(
                query=main_verse,
                translation_id=None, # Will use default
                limit=5
            )
            
            if search_results:
                bible_context += "### Biblical Context (DO NOT INVENT VERSES)\n"
                for v in search_results:
                    bible_context += f"[{v.chapter.book.name} {v.chapter.chapter_number}:{v.verse_number}] {v.text}\n"
                
                # Fetch cross references for the first verse
                if search_results:
                    cross_refs = self.bible_service.cross_reference_service.get_cross_references(str(search_results[0].id))
                    if cross_refs:
                        bible_context += "\n### Cross References\n"
                        for cr in cross_refs[:3]:
                            bible_context += f"- {cr.to_verse.chapter.book.name} {cr.to_verse.chapter.chapter_number}:{cr.to_verse.verse_number}\n"

        # 2. Build Prompt
        prompt = f"""
        You are a seasoned Pastor creating a sermon.
        
        Theme: {theme}
        Audience: {audience}
        Main Text: {main_verse}
        
        {bible_context}
        
        Generate a comprehensive, structured sermon with the following sections using Markdown:
        # [Title]
        ## Big Idea
        ## Introduction
        ## Historical Background
        ## Illustration
        ## Point 1
        ## Point 2
        ## Point 3
        ## Life Application
        ## Challenge
        ## Conclusion
        ## Closing Prayer
        
        Use the provided Biblical context heavily. DO NOT invent any Bible verses.
        Ensure it flows naturally as a spoken sermon.
        """
        
        # 3. Stream Response
        async for chunk in self.gemini_service.generate_content_stream(prompt):
            yield chunk

    async def assist_sermon_stream(self, action: str, current_content: str, selection: Optional[str] = None) -> AsyncGenerator[str, None]:
        """
        Assists with specific tasks like rewrite, expand, simplify.
        """
        prompt = ""
        target_text = selection if selection else current_content
        
        if action == "rewrite":
            prompt = f"Rewrite the following sermon excerpt to flow better and sound more professional:\n\n{target_text}"
        elif action == "expand":
            prompt = f"Expand the following sermon point with more detail and a practical example:\n\n{target_text}"
        elif action == "simplify":
            prompt = f"Simplify the following sermon text so it is easy for anyone to understand (8th-grade reading level):\n\n{target_text}"
        elif action == "illustration":
            prompt = f"Generate a compelling real-life illustration or story that perfectly captures the essence of this point:\n\n{target_text}"
        else:
            prompt = f"Improve this text for a sermon:\n\n{target_text}"
            
        async for chunk in self.gemini_service.generate_content_stream(prompt):
            yield chunk
