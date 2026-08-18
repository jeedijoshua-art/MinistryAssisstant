from PIL import Image, ImageDraw
from app.services.creative.composition.models import DesignSpec

def apply_layout(engine, img: Image.Image, spec: DesignSpec) -> Image.Image:
    width, height = img.size
    
    # Event layout typically has text stacked:
    # Top/Center: Title
    # Below Title: Date, Time, Location
    # We will use a translucent full overlay to ensure readability for event posters
    
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 140)) # 55% opacity full black overlay
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    
    current_y = int(height * 0.15)
    
    if spec.church_name:
        font, txt = engine._fit_text(draw, spec.church_name.upper(), "headline", int(width * 0.8), int(height * 0.1), 40, 24)
        bbox = draw.multiline_textbbox((0, 0), txt, font=font, align="center")
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.multiline_text(((width - w) // 2, current_y), txt, font=font, fill=(200, 200, 200, 255), align="center")
        current_y += h + 40
        
    primary = spec.primary_text or "CHURCH EVENT"
    font, txt = engine._fit_text(draw, primary.upper(), "headline", int(width * 0.9), int(height * 0.3), 120, 48)
    bbox = draw.multiline_textbbox((0, 0), txt, font=font, align="center")
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(((width - w) // 2, current_y), txt, font=font, fill=(255, 255, 255, 255), align="center")
    current_y += h + 60
    
    # details
    details = []
    if spec.date: details.append(f"DATE: {spec.date}")
    if spec.time: details.append(f"TIME: {spec.time}")
    if spec.location: details.append(f"LOCATION: {spec.location}")
    
    if details:
        font = engine._get_font("body", 36)
        for detail in details:
            bbox = draw.textbbox((0, 0), detail, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((width - w) // 2, current_y), detail, font=font, fill=(230, 230, 230, 255))
            current_y += h + 20
            
    if spec.secondary_text:
        current_y += 40
        font, txt = engine._fit_text(draw, spec.secondary_text, "body", int(width * 0.8), int(height * 0.2), 48, 24)
        bbox = draw.multiline_textbbox((0, 0), txt, font=font, align="center")
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.multiline_text(((width - w) // 2, current_y), txt, font=font, fill=(255, 215, 0, 255), align="center") # Gold accent

    return img
