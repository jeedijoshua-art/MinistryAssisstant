import asyncio
import os
import sys

# Setup environment to load fastapi
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv()

from app.database.session import SessionLocal
from app.services.creative.pollinations_service import PollinationsService
from app.services.creative.creative_service import CreativeService
from app.models.domain import GeneratedImage

async def main():
    print("Testing Creative Studio Rebuild...")
    db = SessionLocal()
    pollinations = PollinationsService()
    creative = CreativeService(db, pollinations)

    prompt = "A glowing golden cross on a hill at sunrise, 4k"
    
    print(f"Generating image for prompt: '{prompt}'")
    url = await creative.generate_project_media(prompt=prompt, conversation_id=None, tool_name="test_script")
    
    print(f"Success! Cloudinary URL: {url}")

    print("Checking DB for metadata...")
    img = db.query(GeneratedImage).order_by(GeneratedImage.created_at.desc()).first()
    if img:
        print(f"DB Record Found: ID={img.id}, URL={img.cloudinary_url}, Prompt='{img.prompt}'")
    else:
        print("ERROR: DB Record NOT found!")

if __name__ == "__main__":
    asyncio.run(main())
