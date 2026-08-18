import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    print("Calling Gemini Text API...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Say hello world'
    )
    print("Response:", response.text)
except Exception as e:
    print(f"Exception: {type(e).__name__} - {str(e)}")
