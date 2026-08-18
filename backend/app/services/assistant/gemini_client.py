import logging
import time
from typing import List, Dict, Any, Generator, Optional
from google import genai
from google.genai import types
from google.genai.errors import APIError
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_name = "gemini-3.5-flash-lite"
        
    def _build_contents(self, messages: List[Dict[str, str]]) -> List[types.Content]:
        contents = []
        for msg in messages:
            role = msg.get("role", "user")
            # Gemini roles are 'user' and 'model'
            if role == "assistant":
                role = "model"
            if role == "system":
                # system instructions are passed via config, so we skip here or map to user
                continue
                
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg.get("content", ""))]
                )
            )
        return contents

    def _get_config(self, system_prompt: Optional[str] = None, response_schema: Optional[Any] = None) -> types.GenerateContentConfig:
        config_kwargs = {
            "temperature": 0.7,
            "safety_settings": [
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH
                ),
            ]
        }
        
        if system_prompt:
            config_kwargs["system_instruction"] = system_prompt
            
        if response_schema:
            config_kwargs["response_mime_type"] = "application/json"
            config_kwargs["response_schema"] = response_schema
            
        return types.GenerateContentConfig(**config_kwargs)

    def generate_content(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None,
        response_schema: Optional[Any] = None,
        retries: int = 3
    ) -> str:
        contents = self._build_contents(messages)
        config = self._get_config(system_prompt, response_schema)
        
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=contents,
                    config=config
                )
                return response.text
            except APIError as e:
                logger.warning(f"Gemini API Error (attempt {attempt+1}): {e}")
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)
            except Exception as e:
                logger.error(f"Unexpected Gemini Error: {e}")
                raise

    def generate_content_stream(
        self, 
        messages: List[Dict[str, str]], 
        system_prompt: Optional[str] = None
    ) -> Generator[str, None, None]:
        contents = self._build_contents(messages)
        config = self._get_config(system_prompt)
        
        try:
            response = self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=config
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except APIError as e:
            logger.error(f"Gemini API Stream Error: {e}")
            yield f"\n[Error connecting to AI: {str(e)}]"
        except Exception as e:
            logger.error(f"Unexpected Gemini Stream Error: {e}")
            yield f"\n[Unexpected error: {str(e)}]"
