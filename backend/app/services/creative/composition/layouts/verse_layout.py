from PIL import Image, ImageDraw
from app.services.creative.composition.models import DesignSpec

def apply_layout(engine, img: Image.Image, spec: DesignSpec) -> Image.Image:
    width, height = img.size
    draw = ImageDraw.Draw(img)
    
    # Verse layout wants text in the lower half usually, or center if square.
    # Let's use a subtle dark gradient at the bottom 50%.
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    box_top = int(height * 0.4)
    overlay_draw.rectangle([0, box_top, width, height], fill=(0, 0, 0, 160)) # 60% opacity black
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    
    verse_text = spec.actual_verse_text or spec.primary_text or ""
    reference_text = spec.full_reference or spec.secondary_text or ""
    
    if verse_text:
        max_w = int(width * 0.8)
        max_h = int(height * 0.4)
        
        # Fit main text
        font, wrapped_text = engine._fit_text(draw, verse_text, "body", max_w, max_h, start_size=60, min_size=24)
        
        try:
            text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]
        except AttributeError:
            text_w, text_h = draw.multiline_textsize(wrapped_text, font=font)
            
        text_x = (width - text_w) // 2
        text_y = box_top + (height - box_top - text_h - 100) // 2 # Centered with some bottom padding
        
        draw.multiline_text((text_x, text_y), wrapped_text, font=font, fill=(255, 255, 255, 255), align="center")
        
        if reference_text:
            ref_font = engine._get_font("headline", 36)
            try:
                ref_bbox = draw.textbbox((0, 0), reference_text, font=ref_font)
                ref_w = ref_bbox[2] - ref_bbox[0]
                ref_h = ref_bbox[3] - ref_bbox[1]
            except AttributeError:
                ref_w, ref_h = draw.textsize(reference_text, font=ref_font)
            
            ref_x = (width - ref_w) // 2
            ref_y = text_y + text_h + 40
            
            draw.text((ref_x, ref_y), reference_text, font=ref_font, fill=(200, 200, 200, 255))
            
    return img
