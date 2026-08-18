from typing import Generator
from google import genai  # type: ignore[import-untyped]
from google.genai import types  # type: ignore[import-untyped]
from google.genai.errors import APIError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config import get_settings

class GeminiService:
    def __init__(self):
        settings = get_settings()
        api_key = settings.gemini_api_key
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        self.client = genai.Client(api_key=api_key)
        # We use a default general model for text
        self.default_model = "gemini-3.5-flash-lite"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(APIError)
    )
    def generate_content(
        self,
        system_instruction: str,
        temperature: float = 0.7,
        model: str | None = None,
    ) -> str:
        config = types.GenerateContentConfig(
            temperature=temperature,
        )
        model_name = model or self.default_model
        response = self.client.models.generate_content(
            model=model_name,
            contents=system_instruction,
            config=config,
        )
        return response.text or ""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(APIError)
    )
    def stream_chat(
        self,
        messages: list[dict],
        system_instruction: str | None = None,
        temperature: float = 0.7,
        model: str | None = None,
        tools: list | None = None,
    ) -> Generator[str | dict, None, None]:
        # Convert internal messages dict to genai types
        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
        
        config_kwargs = {
            "temperature": temperature,
            "system_instruction": system_instruction,
        }
        if tools:
            config_kwargs["tools"] = tools

        config = types.GenerateContentConfig(**config_kwargs)

        model_name = model or self.default_model

        # The SDK supports streaming. 
        # Using synchronous stream in an async wrapper for simplicity in FastAPI streaming response
        response = self.client.models.generate_content_stream(
            model=model_name,
            contents=contents,
            config=config,
        )

        for chunk in response:
            if chunk.function_calls:
                for fc in chunk.function_calls:
                    yield {
                        "function_name": fc.name,
                        "function_args": fc.args
                    }
            else:
                try:
                    if chunk.text:
                        yield chunk.text
                except ValueError:
                    pass
