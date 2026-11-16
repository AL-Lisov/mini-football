import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_poster():
    raw_path = 'smm/media/2026-11-16_matchday_myasiko_raw.jpg'
    out_path = 'smm/media/2026-11-16_matchday_myasiko.jpg'
    
    base = Image.open(raw_path).convert('RGBA')
    W, H = base.size # 1024, 1024
    
    # Create an overlay for smooth gradients at top and bottom
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d_overlay = ImageDraw.Draw(overlay)
    
    # Top gradient (fade down from dark)
    for y in range(260):
        alpha = int(220 * (1 - y / 260.0))
        d_overlay.line([(0, y), (W, y)], fill=(10, 11, 14, alpha))
        
    # Bottom gradient (fade up from dark)
    for y in range(H - 420, H):
        progress = (y - (H - 420)) / 420.0
        alpha = int(245 * (progress ** 1.3))
        d_overlay.line([(0, y), (W, y)], fill=(8, 9, 12, alpha))
        
    combined = Image.alpha_composite(base, overlay)
    
    # Fonts
    font_badge = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 20)
    font_league = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
    font_teams = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 44)
    font_vs = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 32)
    font_date = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 54)
    font_venue = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 22)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
    
    draw = ImageDraw.Draw(combined)
    
    # 1. Top Section
    # Matchday badge
    badge_text = "MATCHDAY • 9 ТУР"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0]
    bh = bbox[3] - bbox[1]
    
    badge_x = (W - bw) // 2
    badge_y = 45
    pad_x = 24
    pad_y = 10
    
    # Badge background pill
    draw.rounded_rectangle(
        [(badge_x - pad_x, badge_y - pad_y), (badge_x + bw + pad_x, badge_y + bh + pad_y)],
        radius=20,
        fill=(14, 16, 22, 220),
        outline=(204, 255, 0, 255),
        width=2
    )
    draw.text((badge_x, badge_y - 2), badge_text, font=font_badge, fill=(204, 255, 0))
    
    # League subtitle
    sub_text = "ЧЕМПИОНАТ НИЖНЕГО НОВГОРОДА • ПЕРВАЯ ЛИГА"
    s_bbox = draw.textbbox((0, 0), sub_text, font=font_league)
    sw = s_bbox[2] - s_bbox[0]
    draw.text(((W - sw) // 2, 95), sub_text, font=font_league, fill=(200, 205, 215))
    
    # 2. Match Card in Lower Section
    # Prepare logos
    logo_size = 140
    
    # Doza Agro Logo
    logo_doza = Image.open('img/shields/doza_agro.png').convert('RGBA')
    logo_doza = logo_doza.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    # Myasiko Logo (circular crop with black background)
    logo_myasiko_raw = Image.open('img/shields/myasiko.jpeg').convert('RGBA')
    # Fit into logo_size
    ratio = min(logo_size / logo_myasiko_raw.width, logo_size / logo_myasiko_raw.height)
    new_w = int(logo_myasiko_raw.width * ratio)
    new_h = int(logo_myasiko_raw.height * ratio)
    logo_myasiko_resized = logo_myasiko_raw.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    logo_myasiko = Image.new('RGBA', (logo_size, logo_size), (0, 0, 0, 0))
    logo_myasiko.paste(logo_myasiko_resized, ((logo_size - new_w) // 2, (logo_size - new_h) // 2))
    
    # Card layout
    # Center positions for logos
    y_logos = 650
    cx_left = 260
    cx_right = W - 260
    
    # Circular frames for logos
    frame_r = 82
    # Doza frame
    draw.ellipse(
        [(cx_left - frame_r, y_logos - frame_r), (cx_left + frame_r, y_logos + frame_r)],
        fill=(18, 20, 26, 240),
        outline=(204, 255, 0, 255),
        width=3
    )
    combined.paste(logo_doza, (cx_left - logo_size // 2, y_logos - logo_size // 2), logo_doza)
    
    # Myasiko frame
    draw.ellipse(
        [(cx_right - frame_r, y_logos - frame_r), (cx_right + frame_r, y_logos + frame_r)],
        fill=(18, 20, 26, 240),
        outline=(255, 255, 255, 200),
        width=3
    )
    combined.paste(logo_myasiko, (cx_right - logo_size // 2, y_logos - logo_size // 2), logo_myasiko)
    
    # Team Names under shields
    t1_text = "ДОЗА АГРО"
    t1_bbox = draw.textbbox((0, 0), t1_text, font=font_teams)
    draw.text((cx_left - (t1_bbox[2] - t1_bbox[0]) // 2, y_logos + frame_r + 12), t1_text, font=font_teams, fill=(255, 255, 255))
    
    t2_text = "МЯСИКО"
    t2_bbox = draw.textbbox((0, 0), t2_text, font=font_teams)
    draw.text((cx_right - (t2_bbox[2] - t2_bbox[0]) // 2, y_logos + frame_r + 12), t2_text, font=font_teams, fill=(255, 255, 255))
    
    # VS in the center
    vs_text = "VS"
    vs_bbox = draw.textbbox((0, 0), vs_text, font=font_vs)
    vs_w = vs_bbox[2] - vs_bbox[0]
    draw.text(((W - vs_w) // 2, y_logos - 15), vs_text, font=font_vs, fill=(204, 255, 0))
    
    # Separator line with Neon Volt accent
    line_y = 810
    draw.line([(120, line_y), (W - 120, line_y)], fill=(45, 50, 60, 200), width=1)
    draw.line([(W // 2 - 60, line_y), (W // 2 + 60, line_y)], fill=(204, 255, 0, 255), width=3)
    
    # 3. Match Date & Venue details
    date_text = "16 НОЯБРЯ  |  21:10"
    d_bbox = draw.textbbox((0, 0), date_text, font=font_date)
    dw = d_bbox[2] - d_bbox[0]
    draw.text(((W - dw) // 2, 830), date_text, font=font_date, fill=(204, 255, 0))
    
    venue_text = "ФОК «ПРИОКСКИЙ» • НИЖНИЙ НОВГОРОД"
    v_bbox = draw.textbbox((0, 0), venue_text, font=font_venue)
    vw = v_bbox[2] - v_bbox[0]
    draw.text(((W - vw) // 2, 905), venue_text, font=font_venue, fill=(255, 255, 255))
    
    tag_text = "ВХОД СВОБОДНЫЙ • ПОДДЕРЖИМ БИАНКОНЕРИ НА ТРИБУНАХ"
    t_bbox = draw.textbbox((0, 0), tag_text, font=font_sub)
    tw = t_bbox[2] - t_bbox[0]
    draw.text(((W - tw) // 2, 945), tag_text, font=font_sub, fill=(160, 168, 180))
    
    # Convert to RGB and save high quality
    final_img = combined.convert('RGB')
    final_img.save(out_path, quality=95)
    print(f"Matchday poster successfully created at {out_path}!")

if __name__ == '__main__':
    create_poster()

