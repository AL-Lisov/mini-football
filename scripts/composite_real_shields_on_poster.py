import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import numpy as np

def extract_logo_transparent(img_path, threshold=245):
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img)
    # White background mask
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    # brightness
    brightness = (r.astype(int) + g.astype(int) + b.astype(int)) // 3
    mask = brightness > threshold
    # Smooth alpha near edges
    alpha = np.ones_like(brightness, dtype=np.uint8) * 255
    alpha[mask] = 0
    # anti-alias edge
    edge = (brightness <= threshold) & (brightness > threshold - 25)
    alpha[edge] = ((threshold - brightness[edge]) / 25.0 * 255).astype(np.uint8)
    
    arr[:,:,3] = alpha
    return Image.fromarray(arr)

def process_poster():
    poster_path = "C:/Users/KateLis/.gemini/antigravity/brain/fa191b2b-4fe1-4d7e-8eb5-33906813e88f/doza_agro_progression_poster_1793554101241.jpg"
    base = Image.open(poster_path).convert("RGBA")
    W, H = base.size
    print(f"Base poster size: {W}x{H}")

    # =========================================================================
    # 1. LEFT SHIELD: НИИРТ (Real emblem)
    # Center is approximately (215, 452), radius ~ 125
    # =========================================================================
    niirt_cx, niirt_cy = 217, 450
    niirt_rad = 125
    
    # Load authentic NNIIRT icon
    niirt_src = Image.open("smm/media/nniirt_icon.png").convert("RGBA")
    # Make it a high-res circular badge
    badge_size = 220
    niirt_badge = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(niirt_badge)
    
    # Circular mask for NNIIRT logo
    niirt_resized = niirt_src.resize((badge_size - 10, badge_size - 10), Image.Resampling.LANCZOS)
    offset = 5
    
    # Create mask for circular shape
    c_mask = Image.new("L", (badge_size, badge_size), 0)
    m_draw = ImageDraw.Draw(c_mask)
    m_draw.ellipse((4, 4, badge_size - 4, badge_size - 4), fill=255)
    
    # Paste
    temp = Image.new("RGBA", (badge_size, badge_size), (0, 0, 0, 0))
    temp.paste(niirt_resized, (offset, offset), niirt_resized)
    niirt_badge.paste(temp, (0, 0), c_mask)
    
    # Dark metallic bevel rim around NIIRT to match the poster's metallic shield
    b_draw.ellipse((2, 2, badge_size - 2, badge_size - 2), outline=(100, 160, 200, 180), width=3)
    b_draw.ellipse((5, 5, badge_size - 5, badge_size - 5), outline=(30, 60, 90, 220), width=2)
    
    # Slight battle distress on NIIRT (cracks / fading blue smoke / desaturation)
    # Desaturate slightly to look defeated (4:3)
    enh = ImageEnhance.Color(niirt_badge)
    niirt_badge = enh.enhance(0.85)
    
    # Paste onto base
    nx = niirt_cx - badge_size // 2
    ny = niirt_cy - badge_size // 2
    base.alpha_composite(niirt_badge, (nx, ny))
    
    # Re-apply crack and sparks overlay for NIIRT if needed
    # =========================================================================
    # 2. CENTER SHIELD: DOZA AGRO (Real emblem)
    # Center is approximately (602, 455)
    # On the carbon-fiber shield, replace generic "DOZA AGRO" text with real DA logo
    # =========================================================================
    doza_cx, doza_cy = 602, 448
    doza_w, doza_h = 240, 240
    
    # Load authentic DOZA AGRO shield
    doza_raw = Image.open("img/shields/doza_agro.png").convert("RGBA")
    
    # Clean the circular white badge of DOZA AGRO so it has a crisp border with Neon Volt glow
    scale = 2
    cs = doza_w * scale
    doza_comp = Image.new("RGBA", (cs, cs), (0, 0, 0, 0))
    dc_draw = ImageDraw.Draw(doza_comp)
    
    # White base circle for contrast against the carbon shield
    dc_draw.ellipse((8, 8, cs - 8, cs - 8), fill=(255, 255, 255, 255))
    
    # Neon Volt and dark rim
    dc_draw.ellipse((8, 8, cs - 8, cs - 8), outline=(204, 255, 0, 255), width=8)
    dc_draw.ellipse((16, 16, cs - 16, cs - 16), outline=(15, 20, 25, 255), width=4)
    
    # Inner logo
    pad = 28
    doza_inner = doza_raw.resize((cs - pad*2, cs - pad*2), Image.Resampling.LANCZOS)
    
    mask_in = Image.new("L", (cs, cs), 0)
    mi_draw = ImageDraw.Draw(mask_in)
    mi_draw.ellipse((20, 20, cs - 20, cs - 20), fill=255)
    
    temp_doza = Image.new("RGBA", (cs, cs), (0, 0, 0, 0))
    temp_doza.paste(doza_inner, (pad, pad))
    doza_comp.paste(temp_doza, (0, 0), mask_in)
    
    doza_badge = doza_comp.resize((doza_w, doza_h), Image.Resampling.LANCZOS)
    
    # Add intense Neon Volt glow behind/around the badge to blend with the lightning
    glow_pad = 40
    glow_size = doza_w + glow_pad * 2
    glow_img = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow_img)
    g_draw.ellipse((glow_pad - 10, glow_pad - 10, glow_size - glow_pad + 10, glow_size - glow_pad + 10), fill=(204, 255, 0, 140))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(18))
    
    # Paste glow then badge
    gx = doza_cx - glow_size // 2
    gy = doza_cy - glow_size // 2
    base.alpha_composite(glow_img, (gx, gy))
    
    dx = doza_cx - doza_w // 2
    dy = doza_cy - doza_h // 2
    base.alpha_composite(doza_badge, (dx, dy))

    # =========================================================================
    # 3. RIGHT SHIELD: НГПУ (Real Minin University emblem)
    # Center is approximately (985, 452)
    # Inside the golden crosshair, replace generic torch with real NGPU crest
    # =========================================================================
    ngpu_cx, ngpu_cy = 985, 450
    ngpu_w, ngpu_h = 230, 230
    
    ngpu_raw = Image.open("img/shields/ngpu_minina.png").convert("RGBA")
    
    # Create circular/shield badge for NGPU with golden crosshair aesthetic
    cs = ngpu_w * scale
    ngpu_comp = Image.new("RGBA", (cs, cs), (0, 0, 0, 0))
    nc_draw = ImageDraw.Draw(ngpu_comp)
    
    # White background circle so the crest details pop vividly
    nc_draw.ellipse((8, 8, cs - 8, cs - 8), fill=(255, 255, 255, 255))
    
    # Burnished gold and crimson border matching the crosshairs
    nc_draw.ellipse((8, 8, cs - 8, cs - 8), outline=(220, 180, 70, 255), width=8)
    nc_draw.ellipse((16, 16, cs - 16, cs - 16), outline=(120, 20, 20, 255), width=4)
    
    pad = 24
    ngpu_inner = ngpu_raw.resize((cs - pad*2, cs - pad*2), Image.Resampling.LANCZOS)
    
    mask_ng = Image.new("L", (cs, cs), 0)
    mn_draw = ImageDraw.Draw(mask_ng)
    mn_draw.ellipse((20, 20, cs - 20, cs - 20), fill=255)
    
    temp_ng = Image.new("RGBA", (cs, cs), (0, 0, 0, 0))
    temp_ng.paste(ngpu_inner, (pad, pad))
    ngpu_comp.paste(temp_ng, (0, 0), mask_ng)
    
    ngpu_badge = ngpu_comp.resize((ngpu_w, ngpu_h), Image.Resampling.LANCZOS)
    
    # Subtle crimson & golden target glow behind
    glow_ng = Image.new("RGBA", (glow_size, glow_size), (0, 0, 0, 0))
    gng_draw = ImageDraw.Draw(glow_ng)
    gng_draw.ellipse((glow_pad - 5, glow_pad - 5, glow_size - glow_pad + 5, glow_size - glow_pad + 5), fill=(255, 215, 0, 90))
    glow_ng = glow_ng.filter(ImageFilter.GaussianBlur(15))
    
    base.alpha_composite(glow_ng, (ngpu_cx - glow_size // 2, ngpu_cy - glow_size // 2))
    
    px = ngpu_cx - ngpu_w // 2
    py = ngpu_cy - ngpu_h // 2
    base.alpha_composite(ngpu_badge, (px, py))
    
    # Re-draw the central thin HUD crosshair lines over NGPU so the "target sights" effect stays 100% intact!
    hud_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hud_draw = ImageDraw.Draw(hud_overlay)
    
    # Sights lines
    cross_color = (255, 255, 100, 210)
    # horizontal tick marks
    hud_draw.line([(ngpu_cx - 135, ngpu_cy), (ngpu_cx - 105, ngpu_cy)], fill=cross_color, width=2)
    hud_draw.line([(ngpu_cx + 105, ngpu_cy), (ngpu_cx + 135, ngpu_cy)], fill=cross_color, width=2)
    # vertical tick marks
    hud_draw.line([(ngpu_cx, ngpu_cy - 135), (ngpu_cx, ngpu_cy - 105)], fill=cross_color, width=2)
    hud_draw.line([(ngpu_cx, ngpu_cy + 105), (ngpu_cx, ngpu_cy + 135)], fill=cross_color, width=2)
    
    base = Image.alpha_composite(base, hud_overlay)

    out_file = "smm/media/2026-11-01_next_target_ngpu_epic_real_shields.jpg"
    base.convert("RGB").save(out_file, quality=95)
    print("Saved composite poster:", out_file)

if __name__ == "__main__":
    process_poster()

