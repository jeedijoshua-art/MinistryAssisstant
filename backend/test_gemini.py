from google import genai
from app.config import get_settings
import sys

settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)

models = ['gemini-2.5-flash-lite', 'gemini-3.5-flash-lite', 'gemini-3.5-flash', 'gemini-3.1-pro-preview', 'gemini-flash-lite-latest', 'gemini-2.5-pro']
for m in models:
    try:
        response = client.models.generate_content(
            model=m,
            contents='Hello'
        )
        print(f"Success with {m}: {response.text}")
        sys.exit(0)
    except Exception as e:
        print(f"Failed with {m}: {e}")
