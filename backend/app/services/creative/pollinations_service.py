import httpx
from fastapi import HTTPException
import urllib.parse
import logging

logger = logging.getLogger(__name__)

class PollinationsService:
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt"
    
    async def generate_image(self, prompt: str, width: int = 1080, height: int = 1080) -> bytes:
        """
        Calls Pollinations AI to generate an image from a prompt.
        Returns the raw image bytes.
        """
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"{self.base_url}/{encoded_prompt}?width={width}&height={height}&nologo=true"
        
        logger.info(f"Generating image via Pollinations AI. Prompt: {prompt[:50]}...")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                
                content = response.content
                content_type = response.headers.get("content-type", "unknown")
                byte_size = len(content)
                
                logger.info(f"Pollinations generation: provider=pollinations status=success content_type={content_type} byte_size={byte_size}")
                return content
            except httpx.HTTPStatusError as e:
                logger.error(f"Pollinations generation: provider=pollinations status=failure reason='HTTP {e.response.status_code}'")
                raise HTTPException(status_code=502, detail=f"Image generation failed with status {e.response.status_code}")
            except httpx.RequestError as e:
                logger.error(f"Pollinations generation: provider=pollinations status=failure reason='Network Error'")
                raise HTTPException(status_code=503, detail="Image generation service unavailable")
