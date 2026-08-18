import sys
import logging
from uuid import uuid4
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.assistant.tools.prayer_tool import PrayerTool
from app.services.assistant.content_service import ContentService
from app.services.assistant.gemini_client import GeminiClient

logging.basicConfig(level=logging.INFO)

db = SessionLocal()
try:
    client = GeminiClient()
    content_service = ContentService(db)
    tool = PrayerTool(gemini_client=client, content_service=content_service)
    
    result = tool.execute(user_query="Create a prayer about John 3:16", history=[])
    print(f"RESULT: {result}")
except Exception as e:
    print(f"EXCEPTION: {e}")
finally:
    db.close()
