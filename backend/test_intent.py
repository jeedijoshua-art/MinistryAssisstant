import sys
import logging
from app.services.assistant.intent_detector import IntentDetector
from app.services.assistant.gemini_client import GeminiClient

logging.basicConfig(level=logging.INFO)

client = GeminiClient()
detector = IntentDetector(gemini_client=client)

history = [{"role": "user", "content": "Create a prayer based on it."}]
intent = detector.detect_intent(history)
print(f"DETECTED INTENT: {intent}")
