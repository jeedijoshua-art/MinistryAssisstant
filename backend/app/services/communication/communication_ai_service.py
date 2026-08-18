import asyncio
from typing import Dict, Any, Optional
from app.services.gemini_service import GeminiService
from app.models.domain import Sermon, BrandProfile

class CommunicationAIService:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def generate_platform_asset(self, platform: str, sermon: Sermon, brand: Optional[BrandProfile]) -> str:
        """
        Uses Gemini to generate platform-specific communication copy based on the Sermon.
        """
        theme = getattr(sermon, 'theme', '') or "Christian Worship"
        verse = getattr(sermon, 'main_verse', '') or ""
        audience = getattr(sermon, 'audience', '') or "General Church Audience"
        occasion = getattr(sermon, 'occasion', '') or "Sunday Service"
        title = getattr(sermon, 'title', '') or "Untitled Sermon"
        summary = getattr(sermon, 'content', '')[:1000] if getattr(sermon, 'content') else ""
        
        church_name = brand.church_motto if brand and hasattr(brand, 'church_motto') else "Our Church"
        
        system_instruction = f"""
        You are an expert Church Communications Director and Copywriter.
        Your task is to generate the text for a {platform} based on an upcoming or recently preached sermon.
        
        Context:
        - Sermon Title: {title}
        - Theme: {theme}
        - Main Verse: {verse}
        - Occasion: {occasion}
        - Target Audience: {audience}
        - Church Context: {church_name}
        
        Sermon Snippet:
        {summary}
        """

        if platform == "Instagram Caption":
            system_instruction += "\nGenerate an engaging Instagram caption. Include emojis and 5-7 relevant hashtags. Make it warm and inviting."
        elif platform == "Facebook Caption":
            system_instruction += "\nGenerate a conversational Facebook post. Ask a question to drive engagement. Include emojis."
        elif platform == "WhatsApp Message":
            system_instruction += "\nGenerate a short, friendly WhatsApp broadcast message to invite members to church. Use bolding and emojis."
        elif platform == "Email Newsletter":
            system_instruction += "\nGenerate a 3-paragraph email newsletter. Include a welcoming intro, a summary of the upcoming message, and a clear call to action."
        elif platform == "Church Bulletin":
            system_instruction += "\nGenerate a short, formal paragraph suitable for printing in a physical church bulletin."
        else:
            system_instruction += f"\nGenerate appropriate content for {platform}."
            
        prompt_response = await self.gemini_service.generate_content(system_instruction)
        return prompt_response.strip()
