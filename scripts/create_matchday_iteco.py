import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

def create_badge(img_path, size=(180, 180), border_color=(204, 255, 0), bg_color=(255, 255, 255), radius=22):
    src = Image.open(img_path).convert("RGBA")
    scale = 2
    w, h = size[0] * scale, size[1] * scale
    badge = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    
    # Rounded rectangle background
    draw.rounded_rectangle([(0, 0), (w, h)], radius=radius * scale, fill=bg_color)
    
    # Outer border
    bw = 3 * scale
    for i in range(bw):
        draw.rounded_rectangle([(i, i), (w - i, h - i)], radius=(radius - i//2) * scale, outline=border_color)
        
    badge = badge.resize(size, Image.Resampling.LANCZOS)
    
    # Fit source logo neatly inside
    pad = 12
    max_w = size[0] - pad * 2
    max_h = size[1] - pad * 2
    src.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    
    sw, sh = src.size
    ox = (size[0] - sw) // 2
    oy = (size[1] - sh) // 2
    
    mask = Image.new("L", (w, h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([(bw, bw), (w - bw, h - bw)], radius=(radius - 2) * scale, fill=255)
    mask = mask.resize(size, Image.Resampling.LANCZOS)
    
    content = Image.new("RGBA", size, (0, 0, 0, 0))
    content.paste(src, (ox, oy), src)
    
    badge.paste(content, (0, 0), mask)
    return badge

def build_action_poster():
    raw_path = 'smm/media/2026-11-16_matchday_myasiko_raw.jpg'
    base = Image.open(raw_path).convert('RGBA')
    W, H = base.size # 1024, 1024
    
    # Overlay for contrast gradients at top and bottom
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d_overlay = ImageDraw.Draw(overlay)
    
    # Top gradient
    for y in range(160):
        alpha = int(220 * (1 - y / 160.0) ** 1.1)
        d_overlay.line([(0, y), (W, y)], fill=(8, 10, 14, alpha))
        
    # Bottom gradient (fades up over the floor from y: 490 to H)
    for y in range(480, H):
        prog = (y - 480) / (H - 480.0)
        alpha = int(245 * (prog ** 1.05))
        d_overlay.line([(0, y), (W, y)], fill=(6, 8, 12, alpha))
        
    combined = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(combined)
    
    # Fonts
    font_badge = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 18)
    font_sub_top = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 16)
    font_vs = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 44)
    font_name = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 32)
    font_sub = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 15)
    font_action = ImageFont.truetype('C:/Windows/Fonts/impact.ttf', 44)
    font_details = ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf', 20)
    font_note = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
    
    # 1. TOP BAR
    draw.rectangle([(0, 0), (W, 5)], fill=(204, 255, 0))
    
    badge_text = "ЧЕМПИОНАТ НИЖНЕГО НОВГОРОДА • ПЕРВАЯ ЛИГА"
    bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
    bw = bbox[2] - bbox[0]
    bx = (W - bw) // 2
    by = 28
    draw.rounded_rectangle([(bx - 20, by - 6), (bx + bw + 20, by + 26)], radius=15, fill=(12, 15, 20, 230), outline=(204, 255, 0), width=1)
    draw.text((bx, by), badge_text, font=font_badge, fill=(204, 255, 0))
    
    # 2. LOGOS PLACED ON THE FLOOR
    badge_size = (180, 180)
    card_doza = create_badge('smm/media/logo_doza_agro_authentic.png', size=badge_size, border_color=(204, 255, 0), bg_color=(255, 255, 255), radius=22)
    card_iteco = create_badge('smm/media/logo_iteco_authentic.png', size=badge_size, border_color=(0, 210, 120), bg_color=(0, 105, 62), radius=22)
    
    # Glows
    glow_size = 240
    g_doza = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g_doza)
    gd.rounded_rectangle([(30, 30), (210, 210)], radius=25, fill=(204, 255, 0, 110))
    g_doza = g_doza.filter(ImageFilter.GaussianBlur(22))
    
    g_iteco = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    gi = ImageDraw.Draw(g_iteco)
    gi.rounded_rectangle([(30, 30), (210, 210)], radius=25, fill=(0, 230, 130, 100))
    g_iteco = g_iteco.filter(ImageFilter.GaussianBlur(22))
    
    logo_y = 535
    doza_x = 145
    iteco_x = W - 145 - badge_size[0]
    
    combined.alpha_composite(g_doza, (doza_x - 30, logo_y - 30))
    combined.alpha_composite(g_iteco, (iteco_x - 30, logo_y - 30))
    combined.alpha_composite(card_doza, (doza_x, logo_y))
    combined.alpha_composite(card_iteco, (iteco_x, logo_y))
    
    draw = ImageDraw.Draw(combined)
    
    # VS in center between badges
    vs_bbox = draw.textbbox((0, 0), "VS", font=font_vs)
    vs_w = vs_bbox[2] - vs_bbox[0]
    draw.text(((W - vs_w) // 2, logo_y + 65), "VS", font=font_vs, fill=(204, 255, 0))
    
    # Dark soft pill under sublabels for 100% legibility
    def draw_team_label(team_name, sub_name, x, is_left=True):
        t_box = draw.textbbox((0, 0), team_name, font=font_name)
        s_box = draw.textbbox((0, 0), sub_name, font=font_sub)
        tw = t_box[2] - t_box[0]
        sw = s_box[2] - s_box[0]
        
        center_x = x + badge_size[0] // 2
        tx = center_x - tw // 2
        sx = center_x - sw // 2
        
        # Pill
        pw = max(tw, sw) + 24
        ph = 60
        px = center_x - pw // 2
        py = logo_y + 192
        draw.rounded_rectangle([(px, py), (px + pw, py + ph)], radius=12, fill=(10, 12, 16, 230), outline=(255, 255, 255, 25), width=1)
        
        draw.text((tx, py + 4), team_name, font=font_name, fill=(255, 255, 255))
        sub_col = (160, 235, 220) if is_left else (140, 230, 180)
        draw.text((sx, py + 36), sub_name, font=font_sub, fill=sub_col)

    draw_team_label("ДОЗА АГРО", "комбикормовые заводы", doza_x, is_left=True)
    draw_team_label("ITECO", "CORPORATION", iteco_x, is_left=False)
    
    # 3. BOTTOM SECTION: ATTITUDE & MATCH DETAILS
    bot_y = 815
    
    headline = "БИТВА ЗА ОЧКИ • ТОЛЬКО ПОБЕДА"
    hl_bbox = draw.textbbox((0, 0), headline, font=font_action)
    hl_w = hl_bbox[2] - hl_bbox[0]
    draw.text(((W - hl_w) // 2, bot_y), headline, font=font_action, fill=(204, 255, 0))
    
    venue_text = "ФОК «ПРИОКСКИЙ» • НИЖНИЙ НОВГОРОД • ВХОД СВОБОДНЫЙ"
    v_bbox = draw.textbbox((0, 0), venue_text, font=font_details)
    vw = v_bbox[2] - v_bbox[0]
    vx = (W - vw) // 2
    vy = bot_y + 58
    draw.rounded_rectangle([(vx - 18, vy - 6), (vx + vw + 18, vy + 28)], radius=14, fill=(14, 18, 24, 220), outline=(255, 255, 255, 40), width=1)
    draw.text((vx, vy), venue_text, font=font_details, fill=(255, 255, 255))
    
    note1 = "Прямой стык соседей по таблице (6-е место vs 7-е место)"
    note2 = "Парни выходят на паркет заряженными на 100% — время забирать своё!"
    n1_bbox = draw.textbbox((0, 0), note1, font=font_note)
    n2_bbox = draw.textbbox((0, 0), note2, font=font_note)
    
    draw.text(((W - (n1_bbox[2] - n1_bbox[0])) // 2, vy + 46), note1, font=font_note, fill=(204, 255, 0))
    draw.text(((W - (n2_bbox[2] - n2_bbox[0])) // 2, vy + 72), note2, font=font_note, fill=(180, 195, 215))
    
    foot_text = "МФК «ДОЗА АГРО» • ВКОНТАКТЕ / ТЕЛЕГРАМ"
    f_bbox = draw.textbbox((0, 0), foot_text, font=font_sub_top)
    draw.text(((W - (f_bbox[2] - f_bbox[0])) // 2, H - 35), foot_text, font=font_sub_top, fill=(110, 125, 145))
    
    out_file = 'smm/media/2026-11-23_matchday_iteco.jpg'
    combined.convert('RGB').save(out_file, quality=95)
    print("Action poster saved successfully:", out_file)

if __name__ == "__main__":
    build_action_poster()
