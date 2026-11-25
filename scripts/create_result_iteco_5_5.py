import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_badge(img_path, size=(160, 160), border_color=(204, 255, 0), bg_color=(255, 255, 255), radius=20, trim=6):
    src = Image.open(img_path).convert("RGBA")
    if trim > 0 and src.width > trim * 2 and src.height > trim * 2:
        src = src.crop((trim, trim, src.width - trim, src.height - trim))
    scale = 2
    w, h = size[0] * scale, size[1] * scale
    badge = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)

    draw.rounded_rectangle([(0, 0), (w - 1, h - 1)], radius=radius * scale, fill=bg_color)

    bw = 3 * scale
    for i in range(bw):
        draw.rounded_rectangle([(i, i), (w - 1 - i, h - 1 - i)], radius=(radius - i // 2) * scale, outline=border_color)

    badge = badge.resize(size, Image.Resampling.LANCZOS)

    pad = 8
    max_w = size[0] - pad * 2
    max_h = size[1] - pad * 2
    src.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)

    sw, sh = src.size
    ox = (size[0] - sw) // 2
    oy = (size[1] - sh) // 2

    mask = Image.new("L", (w, h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.rounded_rectangle([(bw, bw), (w - 1 - bw, h - 1 - bw)], radius=(radius - 2) * scale, fill=255)
    mask = mask.resize(size, Image.Resampling.LANCZOS)

    content = Image.new("RGBA", size, (0, 0, 0, 0))
    content.paste(src, (ox, oy), src)

    badge.paste(content, (0, 0), mask)
    return badge

def build_result_poster():
    raw_path = "smm/media/2026-11-25_iteco_5_5_raw.jpg"
    out_path = "smm/media/2026-11-25_iteco_5_5_result.jpg"

    base = Image.open(raw_path).convert("RGBA")
    W, H = base.size  # 1024x1024

    # Gradients for legibility while keeping the center ball & parquet open
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)

    # Top vignette
    for y in range(440):
        alpha = int(195 * (1 - y / 440.0) ** 1.15)
        d_ov.line([(0, y), (W, y)], fill=(8, 10, 14, alpha))

    # Bottom gradient
    for y in range(690, H):
        prog = (y - 690) / float(H - 690)
        alpha = int(240 * (prog ** 1.05))
        d_ov.line([(0, y), (W, y)], fill=(8, 10, 14, alpha))

    combined = Image.alpha_composite(base, overlay)
    draw = ImageDraw.Draw(combined)

    # Fonts
    font_pill = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 17)
    font_score = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 104)
    font_status = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
    font_name = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 30)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
    font_headline = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 48)
    font_desc = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 21)
    font_footer = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 16)

    # Top Neon Volt accent line
    draw.rectangle([(0, 0), (W, 5)], fill=(204, 255, 0))

    # Top tournament pill
    pill_text = "ЧЕМПИОНАТ НИЖНЕГО НОВГОРОДА • ПЕРВАЯ ЛИГА"
    p_box = draw.textbbox((0, 0), pill_text, font=font_pill)
    pw = p_box[2] - p_box[0]
    px = (W - pw) // 2
    py = 42
    draw.rounded_rectangle([(px - 22, py - 7), (px + pw + 22, py + 26)], radius=16, fill=(10, 12, 16, 225), outline=(204, 255, 0), width=1)
    draw.text((px, py - 2), pill_text, font=font_pill, fill=(204, 255, 0))

    # Matchup block in upper half (y: 110..375) - keeps center ball untouched
    badge_size = (165, 165)
    card_doza = create_badge("smm/media/logo_doza_agro_authentic.png", size=badge_size, border_color=(204, 255, 0), bg_color=(254, 254, 254), radius=20, trim=6)
    card_iteco = create_badge("smm/media/logo_iteco_authentic.png", size=badge_size, border_color=(0, 200, 115), bg_color=(2, 111, 80), radius=20, trim=6)

    # Subtle glows behind badges
    glow_size = 225
    g_doza = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    ImageDraw.Draw(g_doza).rounded_rectangle([(30, 30), (195, 195)], radius=24, fill=(204, 255, 0, 75))
    g_doza = g_doza.filter(ImageFilter.GaussianBlur(20))

    g_iteco = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    ImageDraw.Draw(g_iteco).rounded_rectangle([(30, 30), (195, 195)], radius=24, fill=(0, 210, 120, 70))
    g_iteco = g_iteco.filter(ImageFilter.GaussianBlur(20))

    logo_y = 120
    doza_x = 125
    iteco_x = W - 125 - badge_size[0]

    combined.alpha_composite(g_doza, (doza_x - 30, logo_y - 30))
    combined.alpha_composite(g_iteco, (iteco_x - 30, logo_y - 30))
    combined.alpha_composite(card_doza, (doza_x, logo_y))
    combined.alpha_composite(card_iteco, (iteco_x, logo_y))

    draw = ImageDraw.Draw(combined)

    # Center Score "5 : 5"
    score_text = "5 : 5"
    s_box = draw.textbbox((0, 0), score_text, font=font_score)
    sw = s_box[2] - s_box[0]
    sx = (W - sw) // 2
    sy = logo_y + 18

    # Subtle shadow for score
    draw.text((sx + 3, sy + 4), score_text, font=font_score, fill=(0, 0, 0, 200))
    draw.text((sx, sy), score_text, font=font_score, fill=(255, 255, 255))

    # Status pill under score: "ИТОГ МАТЧА • НИЧЬЯ"
    st_text = "ИТОГ МАТЧА • НИЧЬЯ"
    st_box = draw.textbbox((0, 0), st_text, font=font_status)
    stw = st_box[2] - st_box[0]
    stx = (W - stw) // 2
    sty = logo_y + 148
    draw.rounded_rectangle([(stx - 16, sty - 5), (stx + stw + 16, sty + 25)], radius=12, fill=(204, 255, 0))
    draw.text((stx, sty - 2), st_text, font=font_status, fill=(10, 12, 16))

    # Team labels below badges
    def draw_team_label(team_name, sub_name, x, is_left=True):
        t_box = draw.textbbox((0, 0), team_name, font=font_name)
        s_box = draw.textbbox((0, 0), sub_name, font=font_sub)
        tw = t_box[2] - t_box[0]
        sbw = s_box[2] - s_box[0]

        cx = x + badge_size[0] // 2
        tx = cx - tw // 2
        subx = cx - sbw // 2

        pw_box = max(tw, sbw) + 26
        py_box = logo_y + badge_size[1] + 14
        draw.rounded_rectangle([(cx - pw_box // 2, py_box), (cx + pw_box // 2, py_box + 56)], radius=10, fill=(10, 12, 16, 215), outline=(255, 255, 255, 45), width=1)
        draw.text((tx, py_box + 4), team_name, font=font_name, fill=(255, 255, 255))
        sub_col = (180, 235, 225) if is_left else (150, 230, 185)
        draw.text((subx, py_box + 34), sub_name, font=font_sub, fill=sub_col)

    draw_team_label("ДОЗА АГРО", "комбикормовые заводы", doza_x, is_left=True)
    draw_team_label("ITECO", "CORPORATION", iteco_x, is_left=False)

    # Bottom Section (y: 775..1000)
    bot_y = 778

    headline = "ВЕЛИ 5:2 — УПУСТИЛИ ПОБЕДУ"
    h_box = draw.textbbox((0, 0), headline, font=font_headline)
    hw = h_box[2] - h_box[0]
    draw.text(((W - hw) // 2 + 2, bot_y + 3), headline, font=font_headline, fill=(0, 0, 0, 200))
    draw.text(((W - hw) // 2, bot_y), headline, font=font_headline, fill=(204, 255, 0))

    # Crisp white Bianconeri divider line
    div_y = bot_y + 68
    draw.line([(160, div_y), (W - 160, div_y)], fill=(255, 255, 255, 210), width=2)

    desc_text = "Сбились на игру соперника и отдали преимущество. Делаем выводы."
    d_box = draw.textbbox((0, 0), desc_text, font=font_desc)
    dw = d_box[2] - d_box[0]
    draw.text(((W - dw) // 2, div_y + 18), desc_text, font=font_desc, fill=(235, 240, 245))

    foot_text = "ФОК «ПРИОКСКИЙ» • МФК «ДОЗА АГРО»"
    f_box = draw.textbbox((0, 0), foot_text, font=font_footer)
    fw = f_box[2] - f_box[0]
    draw.text(((W - fw) // 2, H - 46), foot_text, font=font_footer, fill=(145, 155, 170))

    combined.convert("RGB").save(out_path, quality=95)
    print("Generated:", out_path)

if __name__ == "__main__":
    build_result_poster()
