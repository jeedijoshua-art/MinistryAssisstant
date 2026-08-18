from uuid import UUID
from sqlalchemy.orm import Session
import cloudinary.uploader
from fastapi import HTTPException

from app.models.domain import GeneratedImage
from app.services.creative.pollinations_service import PollinationsService
from app.config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

class CreativeService:
    def __init__(self, db: Session, pollinations_service: PollinationsService):
        self.db = db
        self.pollinations = pollinations_service
        self.settings = get_settings()
        
        # Configure Cloudinary if keys are present
        if self.settings.cloudinary_cloud_name:
            import cloudinary
            cloudinary.config(
                cloud_name=self.settings.cloudinary_cloud_name,
                api_key=self.settings.cloudinary_api_key,
                api_secret=self.settings.cloudinary_api_secret,
                secure=True
            )

    async def generate_project_media(self, prompt: str, conversation_id: UUID | None, tool_name: str = "creative_studio", image_bytes: bytes = None) -> str:
        """
        Orchestrates the image generation pipeline:
        1. Uses provided bytes OR generates image bytes via Pollinations AI.
        2. Uploads bytes to Cloudinary.
        3. Saves metadata to the Neon database.
        4. Returns the Cloudinary secure URL.
        """
        try:
            # 1. Use provided bytes or generate bytes
            if not image_bytes:
                image_bytes = await self.pollinations.generate_image(prompt, width=1080, height=1350)
            
            # 2. Upload to Cloudinary
            logger.info("Uploading image to Cloudinary...")
            upload_result = cloudinary.uploader.upload(
                image_bytes,
                folder="ztp_assistant/generated",
                resource_type="image"
            )
            secure_url = upload_result.get("secure_url")
            
            if not secure_url:
                raise HTTPException(status_code=500, detail="Cloudinary upload failed to return a secure URL.")
                
            # 3. Save to Neon DB
            logger.info("Saving generated image metadata to database...")
            generated_img = GeneratedImage(
                prompt=prompt,
                provider="pollinations",
                provider_model="flux",
                cloudinary_url=secure_url,
                generation_status="success",
                conversation_id=conversation_id,
                tool_name=tool_name
            )
            self.db.add(generated_img)
            self.db.commit()
            self.db.refresh(generated_img)
            
            # 4. Return URL
            return secure_url
            
        except Exception as e:
            logger.error(f"Failed to generate project media: {str(e)}")
            # Log a failed attempt
            failed_img = GeneratedImage(
                prompt=prompt,
                provider="pollinations",
                provider_model="flux",
                generation_status="failed",
                conversation_id=conversation_id,
                tool_name=tool_name
            )
            self.db.add(failed_img)
            self.db.commit()
            raise HTTPException(status_code=500, detail=f"Creative Service Error: {str(e)}")
