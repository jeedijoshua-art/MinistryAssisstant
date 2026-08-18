import os
from google import genai
from app.config import get_settings

settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)

for m in client.models.list():
    print(m.name)
