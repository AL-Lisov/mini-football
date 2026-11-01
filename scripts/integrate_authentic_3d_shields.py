import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np

from render_3d_emblems import render_doza_monogram, render_nniirt_3d, render_ngpu_3d

def run():
    poster_path = "C:/Users/KateLis/.gemini/antigravity/brain/fa191b2b-4fe1-4d7e-8eb5-33906813e88f/doza_agro_progression_poster_1793554101241.jpg"
    base = Image.open(poster_path).convert("RGBA")
    W, H = base.size
    print(f"Base poster: {W}x{H}")

    # =========================================================================
    # 1. CENTER SHIELD: DOZA AGRO (Integrated 3D Monogram)
    # Center: (602, 448)
    # =========================================================================
    doza_cx, doza_cy = 602, 448
    
    # First: Clean out the generic outline text "DOZA AGRO" from the carbon shield
    # We do this by sampling the carbon fiber texture surrounding it
    carbon_patch = Image.new("RGBA", (280, 200), (20, 25, 30, 255))
    # Fill carbon_patch with a subtle radial gradient matching the shield body
    cp_draw = ImageDraw.Draw(carbon_patch)
    for r in range(140, 0, -2):
        shade = int(22 + (140 - r) * 0.1)
        cp_draw.ellipse((140 - r, 100 - int(r*0.7), 140 + r, 100 + int(r*0.7)), fill=(shade, shade + 4, shade + 8, 255))
        
    # Soft mask for carbon patch so it blends into the shield without hard seams
    patch_mask = Image.new("L", (280, 200), 0)
    pm_draw = ImageDraw.Draw(patch_mask)
    pm_draw.ellipse((20, 15, 260, 185), fill=255)
    patch_mask = patch_mask.filter(ImageFilter.GaussianBlur(15))
    
    # Save original lightning region to re-apply in front
    # Bright green lightning pixels around center:
    base_arr = np.array(base)
    # Green lightning has high G, low B relative to G
    green_mask = (base_arr[:,:,1] > 140) & (base_arr[:,:,1] > base_arr[:,:,0] + 30) & (base_arr[:,:,1] > base_arr[:,:,2] + 40)
    lightning_alpha = np.zeros((H, W), dtype=np.uint8)
    lightning_alpha[green_mask] = 255
    lightning_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lightning_layer.paste(base, (0, 0), Image.fromarray(lightning_alpha))
    
    # Apply soft carbon patch to cleanly erase the generic text
    base.paste(carbon_patch, (doza_cx - 140, doza_cy - 100), patch_mask)
    
    # Render the authentic 3D metallic monogram (size 220)
    mono_size = 230
    doza_3d = render_doza_monogram(size=mono_size)
    
    # Subtle drop shadow behind monogram onto carbon fiber
    shadow = Image.new("RGBA", (mono_size + 20, mono_size + 20), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    mono_alpha = doza_3d.split()[-1].filter(ImageFilter.GaussianBlur(8))
    shadow.paste((0, 0, 0, 180), (10, 14), mono_alpha)
    
    base.alpha_composite(shadow, (doza_cx - mono_size//2 - 10, doza_cy - mono_size//2 - 10))
    base.alpha_composite(doza_3d, (doza_cx - mono_size//2, doza_cy - mono_size//2))
    
    # Re-composite the electric lightning arcing in front of the monogram!
    base.alpha_composite(lightning_layer, (0, 0))

    # =========================================================================
    # 2. LEFT SHIELD: НИИРТ (Integrated 3D Radar Wave Emblem)
    # Center: (217, 450)
    # =========================================================================
    niirt_cx, niirt_cy = 217, 450
    
    # Clean the generic "НИИРТ" text from the center of the radar dish
    dish_patch = Image.new("RGBA", (190, 110), (18, 30, 42, 255))
    dp_draw = ImageDraw.Draw(dish_patch)
    for r in range(95, 0, -2):
        shade = int(18 + (95 - r) * 0.15)
        dp_draw.ellipse((95 - r, 55 - int(r*0.6), 95 + r, 55 + int(r*0.6)), fill=(shade, shade + 8, shade + 18, 255))
        
    dish_mask = Image.new("L", (190, 110), 0)
    dm_draw = ImageDraw.Draw(dish_mask)
    dm_draw.ellipse((15, 10, 175, 100), fill=255)
    dish_mask = dish_mask.filter(ImageFilter.GaussianBlur(12))
    
    base.paste(dish_patch, (niirt_cx - 95, niirt_cy - 55), dish_mask)
    
    # Render authentic 3D NNIIRT radar symbol (size 170)
    niirt_size = 175
    niirt_3d = render_nniirt_3d(size=niirt_size)
    
    # Overlay onto metallic radar dish
    base.alpha_composite(niirt_3d, (niirt_cx - niirt_size//2, niirt_cy - niirt_size//2))
    
    # Add subtle crack overlay across NIIRT to preserve the battle-damaged defeat story (4:3)
    crack_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    co_draw = ImageDraw.Draw(crack_overlay)
    # Fine electric/fracture lines
    co_draw.line([(niirt_cx - 50, niirt_cy - 40), (niirt_cx - 10, niirt_cy), (niirt_cx + 40, niirt_cy + 25)], fill=(200, 240, 255, 160), width=2)
    co_draw.line([(niirt_cx - 10, niirt_cy), (niirt_cx - 5, niirt_cy + 45)], fill=(200, 240, 255, 140), width=1)
    crack_overlay = crack_overlay.filter(ImageFilter.GaussianBlur(1))
    base = Image.alpha_composite(base, crack_overlay)

    # =========================================================================
    # 3. RIGHT SHIELD: НГПУ (Integrated 3D Burnished Gold Seal)
    # Center: (985, 450)
    # =========================================================================
    ngpu_cx, ngpu_cy = 985, 450
    
    # Clean the generic torch/laurel from center of bronze shield
    bronze_patch = Image.new("RGBA", (210, 210), (35, 15, 15, 255))
    bp_draw = ImageDraw.Draw(bronze_patch)
    for r in range(105, 0, -2):
        s_r = int(35 + (105 - r) * 0.25)
        s_g = int(15 + (105 - r) * 0.1)
        s_b = int(12 + (105 - r) * 0.08)
        bp_draw.ellipse((105 - r, 105 - r, 105 + r, 105 + r), fill=(s_r, s_g, s_b, 255))
        
    b_mask = Image.new("L", (210, 210), 0)
    bm_draw = ImageDraw.Draw(b_mask)
    bm_draw.ellipse((20, 20, 190, 190), fill=255)
    b_mask = b_mask.filter(ImageFilter.GaussianBlur(15))
    
    base.paste(bronze_patch, (ngpu_cx - 105, ngpu_cy - 105), b_mask)
    
    # Render authentic 3D Minin University seal in burnished gold (size 195)
    ngpu_size = 195
    ngpu_3d = render_ngpu_3d(size=ngpu_size)
    
    base.alpha_composite(ngpu_3d, (ngpu_cx - ngpu_size//2, ngpu_cy - ngpu_size//2))
    
    # Draw laser HUD crosshairs passing over NGPU (clean sharp yellow lines)
    hud_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hud_overlay)
    
    cross_col = (255, 255, 60, 230)
    cross_glow = (255, 240, 40, 100)
    
    # HUD crosshair circle
    h_draw.ellipse((ngpu_cx - 120, ngpu_cy - 120, ngpu_cx + 120, ngpu_cy + 120), outline=cross_col, width=2)
    # HUD tick lines
    h_draw.line([(ngpu_cx - 150, ngpu_cy), (ngpu_cx - 110, ngpu_cy)], fill=cross_col, width=3)
    h_draw.line([(ngpu_cx + 110, ngpu_cy), (ngpu_cx + 150, ngpu_cy)], fill=cross_col, width=3)
    h_draw.line([(ngpu_cx, ngpu_cy - 150), (ngpu_cx, ngpu_cy - 110)], fill=cross_col, width=3)
    h_draw.line([(ngpu_cx, ngpu_cy + 110), (ngpu_cx, ngpu_cy + 150)], fill=cross_col, width=3)
    
    # Center reticle pip
    h_draw.line([(ngpu_cx - 12, ngpu_cy), (ngpu_cx - 4, ngpu_cy)], fill=cross_col, width=2)
    h_draw.line([(ngpu_cx + 4, ngpu_cy), (ngpu_cx + 12, ngpu_cy)], fill=cross_col, width=2)
    h_draw.line([(ngpu_cx, ngpu_cy - 12), (ngpu_cx, ngpu_cy - 4)], fill=cross_col, width=2)
    h_draw.line([(ngpu_cx, ngpu_cy + 4), (ngpu_cx, ngpu_cy + 12)], fill=cross_col, width=2)
    
    base = Image.alpha_composite(base, hud_overlay)

    # Save final seamless poster
    out_path = "smm/media/2026-11-01_next_target_ngpu_epic_real_shields.jpg"
    base.convert("RGB").save(out_path, quality=96)
    print("Successfully generated seamless 3D integrated poster:", out_path)

if __name__ == "__main__":
    run()

