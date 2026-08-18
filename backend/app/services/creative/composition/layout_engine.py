import io
import textwrap
import logging
from PIL import Image, ImageDraw, ImageFont
from app.services.creative.composition.models import DesignSpec, DesignType

logger = logging.getLogger(__name__)

class LayoutEngine:
    """Core composition engine for overlaying text on generated images."""
    
    def __init__(self):
        # Try to load fonts. Fallback to default if not found.
        self.fonts = {}
        try:
            self.fonts["headline"] = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
            self.fonts["body"] = "/System/Library/Fonts/Supplemental/Arial.ttf"
        except Exception:
            self.fonts["headline"] = None
            self.fonts["body"] = None

    def _get_font(self, font_type: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        font_path = self.fonts.get(font_type)
        if font_path:
            try:
                return ImageFont.truetype(font_path, size=size)
            except Exception:
                pass
        return ImageFont.load_default()
        
    def _fit_text(self, draw: ImageDraw.ImageDraw, text: str, font_path: str, max_width: int, max_height: int, start_size: int = 100, min_size: int = 24) -> tuple[ImageFont.FreeTypeFont, str]:
        """Finds the maximum font size that fits the text into the bounding box, wrapping lines as needed."""
        if not text:
            return self._get_font("body", min_size), ""
            
        current_size = start_size
        
        while current_size >= min_size:
            font = self._get_font(font_path, current_size)
            
            # Approximate char width for this font to guess wrap length
            avg_char_width = sum(draw.textlength(c, font=font) for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") / 52
            if avg_char_width == 0:
                avg_char_width = 10
            
            max_chars = max(1, int(max_width / avg_char_width))
            wrapped_text = textwrap.fill(text, width=max_chars)
            
            try:
                bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
            except AttributeError:
                text_w, text_h = draw.multiline_textsize(wrapped_text, font=font)
                
            if text_w <= max_width and text_h <= max_height:
                return font, wrapped_text
                
            current_size -= 4
            
        # If it still doesn't fit at min_size, we return the min_size and wrapped text anyway
        font = self._get_font(font_path, min_size)
        avg_char_width = sum(draw.textlength(c, font=font) for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") / 52
        if avg_char_width == 0:
            avg_char_width = 10
        max_chars = max(1, int(max_width / avg_char_width))
        wrapped_text = textwrap.fill(text, width=max_chars)
        return font, wrapped_text

    def composite(self, image_bytes: bytes, spec: DesignSpec) -> bytes:
        """Entry point for compositing text onto an image based on the DesignSpec."""
        img = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        width, height = img.size
        
        # Route to specific layout handler
        if spec.design_type == DesignType.VERSE:
            from app.services.creative.composition.layouts.verse_layout import apply_layout
        elif spec.design_type in [DesignType.SERVICE, DesignType.CONFERENCE, DesignType.YOUTH_EVENT]:
            from app.services.creative.composition.layouts.event_layout import apply_layout
        elif spec.design_type == DesignType.EMBLEM:
            from app.services.creative.composition.layouts.emblem_layout import apply_layout
        elif spec.design_type == DesignType.BANNER:
            from app.services.creative.composition.layouts.banner_layout import apply_layout
        else:
            # Default to a generic layout
            from app.services.creative.composition.layouts.verse_layout import apply_layout
            
        try:
            img = apply_layout(self, img, spec)
        except Exception as e:
            logger.error(f"Layout engine failed: {e}")
            # return original if fails
            return image_bytes
            
        final_img = img.convert("RGB")
        out_bytes = io.BytesIO()
        final_img.save(out_bytes, format="JPEG", quality=90)
        return out_bytes.getvalue()
