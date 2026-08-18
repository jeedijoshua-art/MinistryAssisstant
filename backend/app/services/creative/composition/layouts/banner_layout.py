from PIL import Image, ImageDraw
from app.services.creative.composition.models import DesignSpec

def apply_layout(engine, img: Image.Image, spec: DesignSpec) -> Image.Image:
    width, height = img.size
    
    # Banners are wide. We put text in the middle horizontally, or left aligned.
    # Let's do a left-aligned layout with a dark gradient from left to right.
    
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Draw a gradient on the left half
    for x in range(int(width * 0.6)):
        alpha = int(255 - (255 * (x / (width * 0.6))))
        overlay_draw.line([(x, 0), (x, height)], fill=(0, 0, 0, alpha))
        
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    
    left_margin = int(width * 0.05)
    current_y = int(height * 0.2)
    
    if spec.church_name:
        font, txt = engine._fit_text(draw, spec.church_name.upper(), "headline", int(width * 0.4), int(height * 0.1), 40, 24)
        draw.text((left_margin, current_y), txt, font=font, fill=(200, 200, 200, 255))
        try:
            bbox = draw.textbbox((0, 0), txt, font=font)
            current_y += bbox[3] - bbox[1] + 20
        except AttributeError:
            current_y += 50
            
    primary = spec.primary_text or "CHURCH BANNER"
    font, txt = engine._fit_text(draw, primary.upper(), "headline", int(width * 0.5), int(height * 0.4), 100, 36)
    draw.multiline_text((left_margin, current_y), txt, font=font, fill=(255, 255, 255, 255))
    
    try:
        bbox = draw.multiline_textbbox((0, 0), txt, font=font)
        current_y += bbox[3] - bbox[1] + 40
    except AttributeError:
        current_y += 120
        
    if spec.secondary_text:
        font, txt = engine._fit_text(draw, spec.secondary_text, "body", int(width * 0.4), int(height * 0.2), 48, 24)
        draw.multiline_text((left_margin, current_y), txt, font=font, fill=(255, 215, 0, 255))
        
    return img
