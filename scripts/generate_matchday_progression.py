import os
from PIL import Image, ImageDraw, ImageFont

def create_circular_badge(img_path, size, border_color=(204, 255, 0), border_width=4, bg_color=(255, 255, 255)):
    src = Image.open(img_path).convert("RGBA")
    
    scale = 2
    canvas_size = size * scale
    badge = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    
    # Background circle
    draw.ellipse((0, 0, canvas_size - 1, canvas_size - 1), fill=bg_color)
    
    # Border circle
    if border_width > 0:
        bw = border_width * scale
        for i in range(bw):
            draw.ellipse((i, i, canvas_size - 1 - i, canvas_size - 1 - i), outline=border_color)
            
    badge = badge.resize((size, size), Image.Resampling.LANCZOS)
    
    # Fit source image neatly
    pad = border_width + 12
    max_src_size = size - (pad * 2)
    src.thumbnail((max_src_size, max_src_size), Image.Resampling.LANCZOS)
    
    src_w, src_h = src.size
    offset_x = (size - src_w) // 2
    offset_y = (size - src_h) // 2
    
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((border_width, border_width, size - border_width, size - border_width), fill=255)
    
    temp = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    temp.paste(src, (offset_x, offset_y), src)
    
    badge.paste(temp, (0, 0), mask)
    return badge

def generate_vertical_poster():
    W, H = 1080, 1350
    img = Image.new("RGBA", (W, H), (10, 12, 16, 255))
    draw = ImageDraw.Draw(img)
    
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 68)
    font_score = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 76)
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 28)
    font_name = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 24)
    font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 20)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 22)
    
    # Gradient background
    for y in range(H):
        r = int(10 + (y / H) * 12)
        g = int(12 + (y / H) * 14)
        b = int(16 + (y / H) * 18)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    # Subtle Bianconeri diagonal stripes
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    for x in range(-500, W + 500, 180):
        ov_draw.polygon([(x, 0), (x + 80, 0), (x - 220, H), (x - 300, H)], fill=(255, 255, 255, 5))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Top neon line
    draw.rectangle([(0, 0), (W, 6)], fill=(204, 255, 0))
    
    # Top bar
    draw.rounded_rectangle([(60, 45), (320, 85)], radius=20, outline=(204, 255, 0), width=1)
    draw.text((85, 53), "МФК «ДОЗА АГРО»", font=font_tag, fill=(204, 255, 0))
    draw.text((W - 270, 53), "MATCHDAY TRANSITION", font=font_tag, fill=(160, 170, 185))
    
    # Titles
    draw.text((60, 110), "ОДИН РУБЕЖ ВЗЯТ", font=font_title, fill=(255, 255, 255))
    draw.text((60, 185), "СЛЕДУЮЩИЙ — НГПУ", font=font_title, fill=(204, 255, 0))
    
    draw.line([(60, 270), (W - 60, 270)], fill=(255, 255, 255, 40), width=1)
    
    # ---------------- CARD 1: NIIRT ----------------
    card1_y = 295
    card1_h = 360
    draw.rounded_rectangle([(60, card1_y), (W - 60, card1_y + card1_h)], radius=16, fill=(18, 22, 30, 240), outline=(255, 255, 255, 25), width=1)
    
    draw.rounded_rectangle([(85, card1_y + 25), (370, card1_y + 60)], radius=6, fill=(28, 35, 48))
    draw.text((105, card1_y + 30), "СУПЕРЛИГА NML · 3 ТУР", font=font_tag, fill=(180, 195, 215))
    
    draw.rounded_rectangle([(W - 280, card1_y + 25), (W - 85, card1_y + 60)], radius=6, fill=(204, 255, 0))
    draw.text((W - 260, card1_y + 30), "ПОБЕДА 4 : 3", font=font_tag, fill=(12, 15, 20))
    
    # Original badges
    badge_niirt = create_circular_badge("smm/media/nniirt_icon.png", 140, border_color=(100, 115, 135), border_width=3)
    badge_doza = create_circular_badge("img/shields/doza_agro.png", 140, border_color=(204, 255, 0), border_width=4)
    
    img.paste(badge_niirt, (130, card1_y + 85), badge_niirt)
    img.paste(badge_doza, (W - 270, card1_y + 85), badge_doza)
    
    draw.text((W // 2 - 80, card1_y + 110), "3 : 4", font=font_score, fill=(255, 255, 255))
    draw.text((W // 2 - 45, card1_y + 195), "ФИНАЛ", font=font_tag, fill=(140, 155, 175))
    
    draw.text((165, card1_y + 245), "НИИРТ", font=font_name, fill=(160, 175, 195))
    draw.text((W - 305, card1_y + 245), "DOZA AGRO", font=font_name, fill=(204, 255, 0))
    
    draw.line([(85, card1_y + 295), (W - 85, card1_y + 295)], fill=(255, 255, 255, 20), width=1)
    draw.text((85, card1_y + 312), "Тяжелая валидольная победа. Новичок Роман «Коновал» Коновалов решил моменты!", font=font_small, fill=(200, 210, 225))

    # ---------------- TRANSITION STRIP ----------------
    trans_y = 680
    draw.rounded_rectangle([(60, trans_y), (W - 60, trans_y + 55)], radius=10, fill=(204, 255, 0))
    draw.text((90, trans_y + 12), "СЛЕДУЮЩИЙ РУБЕЖ // NEXT TARGET: НГПУ — ВЫ СЛЕДУЮЩИЕ", font=font_bold, fill=(12, 15, 20))

    # ---------------- CARD 2: NGPU ----------------
    card2_y = 760
    card2_h = 470
    draw.rounded_rectangle([(60, card2_y), (W - 60, card2_y + card2_h)], radius=16, fill=(18, 22, 30, 240), outline=(204, 255, 0), width=2)
    
    draw.rounded_rectangle([(85, card2_y + 25), (420, card2_y + 60)], radius=6, fill=(28, 35, 48))
    draw.text((105, card2_y + 30), "ПЕРВАЯ ЛИГА · 4 ТУР", font=font_tag, fill=(204, 255, 0))
    
    draw.rounded_rectangle([(W - 270, card2_y + 25), (W - 85, card2_y + 60)], radius=6, outline=(255, 255, 255, 60), width=1)
    draw.text((W - 250, card2_y + 30), "2 НОЯБРЯ · 21:10", font=font_tag, fill=(255, 255, 255))
    
    badge_doza2 = create_circular_badge("img/shields/doza_agro.png", 170, border_color=(204, 255, 0), border_width=4)
    badge_ngpu = create_circular_badge("img/shields/ngpu_minina.png", 170, border_color=(255, 255, 255), border_width=4)
    
    img.paste(badge_doza2, (130, card2_y + 95), badge_doza2)
    img.paste(badge_ngpu, (W - 300, card2_y + 95), badge_ngpu)
    
    draw.text((W // 2 - 40, card2_y + 145), "VS", font=font_score, fill=(204, 255, 0))
    
    draw.text((140, card2_y + 285), "ДОЗА АГРО", font=font_bold, fill=(255, 255, 255))
    draw.text((W - 265, card2_y + 285), "НГПУ", font=font_bold, fill=(255, 255, 255))
    
    draw.line([(85, card2_y + 345), (W - 85, card2_y + 345)], fill=(255, 255, 255, 20), width=1)
    draw.text((85, card2_y + 365), "ФОК «Приокский» · Соперник мощнейший, сладко не будет!", font=font_bold, fill=(204, 255, 0))
    draw.text((85, card2_y + 405), "Наш ответ — прессинг, характер и борьба за каждый метр паркета.", font=font_small, fill=(180, 190, 205))

    # Footer
    draw.text((W // 2 - 160, H - 45), "МФК «ДОЗА АГРО» · ОФИЦИАЛЬНО", font=font_tag, fill=(110, 120, 135))

    out_path = "smm/media/2026-11-01_next_target_ngpu_authentic.jpg"
    img.convert("RGB").save(out_path, quality=95)
    print("Vertical poster generated:", out_path)

def generate_horizontal_banner():
    W, H = 1200, 675
    img = Image.new("RGBA", (W, H), (10, 12, 16, 255))
    draw = ImageDraw.Draw(img)
    
    font_title = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 46)
    font_score = ImageFont.truetype(r"C:\Windows\Fonts\impact.ttf", 60)
    font_bold = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 24)
    font_name = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 20)
    font_tag = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 16)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 16)
    
    # Gradient
    for y in range(H):
        r = int(10 + (y / H) * 12)
        g = int(12 + (y / H) * 14)
        b = int(16 + (y / H) * 18)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
        
    draw.rectangle([(0, 0), (W, 4)], fill=(204, 255, 0))
    
    # Header
    draw.text((50, 25), "ОДИН РУБЕЖ ВЗЯТ // СЛЕДУЮЩИЙ — НГПУ", font=font_title, fill=(255, 255, 255))
    draw.text((W - 240, 35), "МФК «ДОЗА АГРО»", font=font_bold, fill=(204, 255, 0))
    
    draw.line([(50, 85), (W - 50, 85)], fill=(255, 255, 255, 40), width=1)
    
    # 2 side-by-side cards: Left (Played 4:3) vs Right (Next match 21:10)
    card_w = 525
    card_h = 515
    y_start = 110
    
    # CARD 1: NIIRT
    c1_x = 50
    draw.rounded_rectangle([(c1_x, y_start), (c1_x + card_w, y_start + card_h)], radius=14, fill=(18, 22, 30, 240), outline=(255, 255, 255, 25), width=1)
    
    draw.rounded_rectangle([(c1_x + 25, y_start + 20), (c1_x + 260, y_start + 50)], radius=4, fill=(28, 35, 48))
    draw.text((c1_x + 35, y_start + 25), "СУПЕРЛИГА NML · 3 ТУР", font=font_tag, fill=(180, 195, 215))
    
    draw.rounded_rectangle([(c1_x + card_w - 180, y_start + 20), (c1_x + card_w - 25, y_start + 50)], radius=4, fill=(204, 255, 0))
    draw.text((c1_x + card_w - 165, y_start + 25), "ПОБЕДА 4 : 3", font=font_tag, fill=(12, 15, 20))
    
    b_niirt = create_circular_badge("smm/media/nniirt_icon.png", 125, border_color=(100, 115, 135), border_width=3)
    b_doza1 = create_circular_badge("img/shields/doza_agro.png", 125, border_color=(204, 255, 0), border_width=4)
    
    img.paste(b_niirt, (c1_x + 40, y_start + 85), b_niirt)
    img.paste(b_doza1, (c1_x + card_w - 165, y_start + 85), b_doza1)
    
    draw.text((c1_x + card_w // 2 - 55, y_start + 115), "3 : 4", font=font_score, fill=(255, 255, 255))
    draw.text((c1_x + card_w // 2 - 30, y_start + 185), "ФИНАЛ", font=font_tag, fill=(140, 155, 175))
    
    draw.text((c1_x + 70, y_start + 230), "НИИРТ", font=font_name, fill=(160, 175, 195))
    draw.text((c1_x + card_w - 165, y_start + 230), "DOZA AGRO", font=font_name, fill=(204, 255, 0))
    
    draw.line([(c1_x + 25, y_start + 280), (c1_x + card_w - 25, y_start + 280)], fill=(255, 255, 255, 20), width=1)
    draw.text((c1_x + 25, y_start + 300), "Тяжелейшие 4:3 на морально-волевых.", font=font_bold, fill=(255, 255, 255))
    draw.text((c1_x + 25, y_start + 340), "Дебют новичка: Роман «Коновал» Коновалов", font=font_small, fill=(204, 255, 0))
    draw.text((c1_x + 25, y_start + 370), "хладнокровно зарешал свои моменты и принес победу!", font=font_small, fill=(180, 195, 215))
    
    # CARD 2: NEXT MATCH (NGPU)
    c2_x = W - 50 - card_w
    draw.rounded_rectangle([(c2_x, y_start), (c2_x + card_w, y_start + card_h)], radius=14, fill=(18, 22, 30, 240), outline=(204, 255, 0), width=2)
    
    draw.rounded_rectangle([(c2_x + 25, y_start + 20), (c2_x + 260, y_start + 50)], radius=4, fill=(28, 35, 48))
    draw.text((c2_x + 35, y_start + 25), "ПЕРВАЯ ЛИГА · 4 ТУР", font=font_tag, fill=(204, 255, 0))
    
    draw.rounded_rectangle([(c2_x + card_w - 190, y_start + 20), (c2_x + card_w - 25, y_start + 50)], radius=4, outline=(255, 255, 255, 60), width=1)
    draw.text((c2_x + card_w - 175, y_start + 25), "2 НОЯБРЯ · 21:10", font=font_tag, fill=(255, 255, 255))
    
    b_doza2 = create_circular_badge("img/shields/doza_agro.png", 130, border_color=(204, 255, 0), border_width=4)
    b_ngpu = create_circular_badge("img/shields/ngpu_minina.png", 130, border_color=(255, 255, 255), border_width=4)
    
    img.paste(b_doza2, (c2_x + 40, y_start + 85), b_doza2)
    img.paste(b_ngpu, (c2_x + card_w - 170, y_start + 85), b_ngpu)
    
    draw.text((c2_x + card_w // 2 - 30, y_start + 120), "VS", font=font_score, fill=(204, 255, 0))
    
    draw.text((c2_x + 45, y_start + 230), "ДОЗА АГРО", font=font_bold, fill=(255, 255, 255))
    draw.text((c2_x + card_w - 145, y_start + 230), "НГПУ", font=font_bold, fill=(255, 255, 255))
    
    draw.line([(c2_x + 25, y_start + 280), (c2_x + card_w - 25, y_start + 280)], fill=(255, 255, 255, 20), width=1)
    draw.text((c2_x + 25, y_start + 300), "НГПУ — ВЫ СЛЕДУЮЩИЕ!", font=font_bold, fill=(204, 255, 0))
    draw.text((c2_x + 25, y_start + 340), "ФОК «Приокский» · Время: 21:10", font=font_small, fill=(255, 255, 255))
    draw.text((c2_x + 25, y_start + 370), "Один из лидеров турнира. Сладко не будет, выходим биться!", font=font_small, fill=(180, 195, 215))

    out_path = "smm/media/2026-11-01_next_target_ngpu_banner.jpg"
    img.convert("RGB").save(out_path, quality=95)
    print("Horizontal banner generated:", out_path)

if __name__ == "__main__":
    generate_vertical_poster()
    generate_horizontal_banner()
