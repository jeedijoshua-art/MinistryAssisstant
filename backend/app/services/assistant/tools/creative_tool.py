import asyncio
import io
import json
import logging
from uuid import UUID
from app.services.assistant.tools.base_tool import BaseTool
from app.services.creative.creative_service import CreativeService
from app.services.creative.pollinations_service import PollinationsService
from app.services.assistant.content_service import ContentService
from app.services.bible.bible_service import BibleService
from app.services.assistant.gemini_client import GeminiClient
from app.services.creative.composition.models import DesignSpec, DesignType, Orientation
from app.services.creative.composition.layout_engine import LayoutEngine

logger = logging.getLogger(__name__)

class CreativeStudioTool(BaseTool):
    """
    Assistant tool that hooks into the agent pipeline to generate imagery.
    Orchestrates the image generation by classifying design intent, calling Pollinations, 
    and compositing text intelligently via the LayoutEngine.
    """
    def __init__(self, gemini_client: GeminiClient, content_service: ContentService, bible_service: BibleService):
        self.gemini_client = gemini_client
        self.content_service = content_service
        self.bible_service = bible_service
        self.layout_engine = LayoutEngine()

    @property
    def name(self) -> str:
        return "creative_studio_tool"

    @property
    def description(self) -> str:
        return "Generate posters, banners, social media graphics, emblems, and other visual creative assets. Executes an intelligent design process to match intent to layout."

    def execute(self, user_query: str, history: list, **kwargs) -> str:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(self._execute_async(user_query, history))

    async def _execute_async(self, prompt: str, history: list) -> str:
        db = self.content_service.db
        pollinations_service = PollinationsService()
        creative_service = CreativeService(db, pollinations_service)
        
        # 1. Use Gemini to extract DesignSpec
        extract_instruction = """
        You are an expert graphic designer and intent detector. Parse the user's request for a poster, banner, or graphic.
        Return a JSON object conforming strictly to the DesignSpec schema.
        IMPORTANT: In 'visual_prompt', generate a highly detailed visual art direction prompt. Explicitly add: 'Generate the artwork/background only. Do NOT render any readable text. Do NOT generate Bible verses. Do NOT generate typography. Do NOT generate letters, words, captions, watermarks, logos, or scripture text.'
        Determine the most appropriate 'design_type' and 'orientation'. Banners should be 'landscape', posters 'portrait'. Emblems/logos should be 'square'.
        Extract any event details if present. Extract Bible reference if present.
        """
        
        try:
            args_json = self.gemini_client.generate_content(
                messages=[{"role": "user", "content": f"Request: {prompt}"}],
                system_prompt=extract_instruction,
                response_schema=DesignSpec
            )
            spec_dict = json.loads(args_json)
            spec = DesignSpec(**spec_dict)
        except Exception as e:
            logger.warning(f"Failed to parse DesignSpec with Gemini: {e}")
            spec = DesignSpec(
                design_type=DesignType.GENERAL,
                orientation=Orientation.PORTRAIT,
                width=1080,
                height=1350,
                visual_theme="general",
                visual_prompt=f"Beautiful, cinematic, masterpiece. No text, no typography. {prompt}"
            )

        # Map orientation to dimensions
        if spec.orientation == Orientation.LANDSCAPE:
            spec.width, spec.height = 1920, 1080
            # Pollinations might have limits, so let's stick to safe bounds
        elif spec.orientation == Orientation.SQUARE:
            spec.width, spec.height = 1080, 1080
        else:
            spec.width, spec.height = 1080, 1350

        # 2. Fetch Bible verse if present
        if spec.has_bible_reference and spec.bible_reference:
            verses = self.bible_service.resolve_reference(spec.bible_reference, spec.translation)
            if verses:
                verse_text = " ".join([v.text for v in verses])
                if len(verse_text) > 800:
                    verse_text = verse_text[:797] + "..."
                spec.actual_verse_text = verse_text
                
                full_reference = f"— {verses[0].chapter.book.name} {verses[0].chapter.chapter_number}:{verses[0].verse_number}"
                if len(verses) > 1:
                    full_reference += f"-{verses[-1].verse_number}"
                full_reference += f" {spec.translation.upper()}"
                spec.full_reference = full_reference

        # 3. Generate base image via Pollinations
        try:
            image_bytes = await pollinations_service.generate_image(spec.visual_prompt, width=spec.width, height=spec.height)
        except Exception as e:
            return f"Failed to generate base artwork. Error: {str(e)}"
            
        # 4. Composite Text using LayoutEngine
        try:
            image_bytes = self.layout_engine.composite(image_bytes, spec)
        except Exception as e:
            logger.error(f"Failed to composite typography: {e}")

        # 5. Upload to Cloudinary and Save to DB
        try:
            image_url = await creative_service.generate_project_media(
                prompt=prompt,
                conversation_id=None,
                tool_name=self.name,
                image_bytes=image_bytes
            )
            
            return f"""
Successfully generated image!

[SYSTEM INSTRUCTION: YOU MUST OUTPUT THE FOLLOWING EXACT MARKDOWN IN YOUR FINAL RESPONSE SO THE USER CAN SEE THE IMAGE. DO NOT OMIT IT.]

![{prompt}]({image_url})
"""
        except Exception as e:
            return f"Failed to upload and save image. Error: {str(e)}"
