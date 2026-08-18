from PIL import Image, ImageDraw
from app.services.creative.composition.models import DesignSpec

def apply_layout(engine, img: Image.Image, spec: DesignSpec) -> Image.Image:
    width, height = img.size
    
    # Emblems are usually square. The symbol is in the center.
    # We put the church name around or under the emblem.
    
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # subtle radial or bottom gradient
    box_top = int(height * 0.7)
    overlay_draw.rectangle([0, box_top, width, height], fill=(0, 0, 0, 160)) 
    
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    
    current_y = int(height * 0.75)
    
    if spec.church_name:
        font, txt = engine._fit_text(draw, spec.church_name.upper(), "headline", int(width * 0.9), int(height * 0.15), 80, 32)
        bbox = draw.multiline_textbbox((0, 0), txt, font=font, align="center")
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.multiline_text(((width - w) // 2, current_y), txt, font=font, fill=(255, 255, 255, 255), align="center")
        current_y += h + 20
        
    if spec.tagline:
        font, txt = engine._fit_text(draw, spec.tagline.upper(), "body", int(width * 0.8), int(height * 0.1), 40, 20)
        bbox = draw.multiline_textbbox((0, 0), txt, font=font, align="center")
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.multiline_text(((width - w) // 2, current_y), txt, font=font, fill=(200, 200, 200, 255), align="center")

    return img
