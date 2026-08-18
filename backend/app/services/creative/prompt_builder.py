import json
from typing import Dict, Any, Optional
from app.services.gemini_service import GeminiService
from app.models.domain import Sermon, BrandProfile

class PromptBuilderService:
    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service

    async def build_image_prompt(self, media_type: str, sermon: Optional[Sermon], brand: BrandProfile, override_theme: Optional[str] = None) -> str:
        """
        Uses Gemini to generate an optimized prompt for image generation based on Sermon context and Brand Profile.
        """
        theme = override_theme or getattr(sermon, 'theme', '') or "Christian Worship"
        verse = getattr(sermon, 'main_verse', '') or ""
        audience = getattr(sermon, 'audience', '') or "General Church Audience"
        occasion = getattr(sermon, 'occasion', '') or "Sunday Service"
        
        # Build context for Gemini
        system_instruction = f"""
        You are an expert AI prompt engineer specializing in Christian church media and graphic design.
        Your task is to generate a highly detailed, comma-separated prompt for an image generation AI (like Midjourney or DALL-E) to create a background image for a {media_type}.
        
        Do NOT include any text, words, or typography in the image prompt itself, as text will be overlaid later by our editor.
        The image should serve as a beautiful, atmospheric background.
        
        Context:
        - Theme: {theme}
        - Main Verse: {verse}
        - Occasion: {occasion}
        - Target Audience: {audience}
        
        Brand Guidelines:
        - Primary Color: {brand.primary_color}
        - Secondary Color: {brand.secondary_color}
        
        Output ONLY the raw image generation prompt string.
        Example output: "dramatic landscape of a calm sea at sunrise, soft golden hour lighting, cinematic composition, empty space in center for text, ethereal atmosphere, high resolution, 8k, --ar 4:5"
        """
        
        import asyncio
        prompt_response = await asyncio.to_thread(self.gemini_service.generate_content, system_instruction)
        return prompt_response.strip()
