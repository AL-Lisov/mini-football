import os
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps
import numpy as np

def create_metallic_relief(mask_img, base_color=(200, 200, 200), highlight_color=(255, 255, 255), shadow_color=(30, 30, 30), depth=2):
    # mask_img is RGBA where alpha is the shape
    alpha = np.array(mask_img.split()[-1], dtype=float) / 255.0
    
    # Generate bevel / 3D relief using directional gradient
    # light comes from top-left (dx, dy)
    dx = np.roll(alpha, 1, axis=1) - np.roll(alpha, -1, axis=1)
    dy = np.roll(alpha, 1, axis=0) - np.roll(alpha, -1, axis=0)
    
    # Top-left light direction: (-0.5, -0.7)
    light = -0.5 * dx - 0.7 * dy
    light = np.clip(light * depth * 3.0, -1.0, 1.0)
    
    h, w = alpha.shape
    res = np.zeros((h, w, 4), dtype=np.uint8)
    
    # Calculate color per pixel
    for i in range(3):
        c_base = base_color[i]
        c_high = highlight_color[i]
        c_shad = shadow_color[i]
        
        # Where light > 0: blend towards highlight
        col = np.where(light > 0, 
                       c_base + (c_high - c_base) * light,
                       c_base + (c_base - c_shad) * light)
        res[:,:,i] = np.clip(col, 0, 255).astype(np.uint8)
        
    res[:,:,3] = (alpha * 255).astype(np.uint8)
    return Image.fromarray(res)

def render_doza_monogram(size=300):
    # Size 300x300
    # The Doza Agro monogram consists of:
    # 1. An upward-pointing chevron 'A' (dark titanium with neon volt glow)
    # 2. An inverted chevron / triangle 'V' interlaced (neon volt / teal with metallic edge)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    cx, cy = size // 2, size // 2
    
    # Chevron dimensions
    w_half = 75
    h_half = 95
    th = 26 # stroke thickness
    
    # Upward Chevron 'A' (Left & apex)
    # Points: Apex top (cx - 20, cy - h_half), Bottom-left (cx - w_half - 20, cy + h_half), etc.
    # Let's draw precise polygons for the sharp geometric interlocking chevrons
    
    # Chevron 1 (Upward, A): Apex at (cx - 15, cy - 80)
    p_up_out = [
        (cx - 15, cy - 85),
        (cx + 45, cy + 85),
        (cx + 15, cy + 85),
        (cx - 15, cy - 25),
        (cx - 45, cy + 85),
        (cx - 75, cy + 85)
    ]
    
    # Chevron 2 (Downward, V / D): Apex at (cx + 15, cy + 85)
    p_down_out = [
        (cx + 15, cy + 85),
        (cx - 45, cy - 85),
        (cx - 15, cy - 85),
        (cx + 15, cy + 25),
        (cx + 45, cy - 85),
        (cx + 75, cy - 85)
    ]
    
    # Draw chevrons on high-res mask (scale 4x for extreme crispness)
    scale = 4
    mask_hr = Image.new("L", (size * scale, size * scale), 0)
    d_hr = ImageDraw.Draw(mask_hr)
    
    def scale_poly(pts):
        return [(x * scale, y * scale) for (x, y) in pts]
        
    d_hr.polygon(scale_poly(p_up_out), fill=255)
    d_hr.polygon(scale_poly(p_down_out), fill=255)
    
    mask = mask_hr.resize((size, size), Image.Resampling.LANCZOS)
    
    # Create 3D metallic titanium relief for the monogram
    # Base: dark carbon-titanium (45, 55, 60), Highlight: (230, 255, 220), Shadow: (10, 15, 20)
    mono_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    mono_img.putalpha(mask)
    
    relief = create_metallic_relief(mono_img, base_color=(35, 42, 48), highlight_color=(200, 255, 120), shadow_color=(10, 14, 18), depth=3)
    
    # Draw vibrant Neon Volt glowing border along the outer edges of the chevrons
    edge = mask.filter(ImageFilter.FIND_EDGES)
    edge_glow = edge.filter(ImageFilter.GaussianBlur(3))
    
    glow_arr = np.array(edge_glow)
    glow_rgba = np.zeros((size, size, 4), dtype=np.uint8)
    glow_rgba[:,:,0] = 204 # Neon Volt R
    glow_rgba[:,:,1] = 255 # Neon Volt G
    glow_rgba[:,:,2] = 0   # Neon Volt B
    glow_rgba[:,:,3] = (glow_arr * 0.9).astype(np.uint8)
    
    glow_layer = Image.fromarray(glow_rgba)
    
    # Composite relief with neon glow edges
    final_mono = Image.alpha_composite(glow_layer, relief)
    
    # Add crisp 1px neon highlight on edges
    crisp_edge = edge.point(lambda p: 255 if p > 80 else 0)
    edge_rgba = np.zeros((size, size, 4), dtype=np.uint8)
    edge_rgba[:,:,0] = 204
    edge_rgba[:,:,1] = 255
    edge_rgba[:,:,2] = 0
    edge_rgba[:,:,3] = np.array(crisp_edge)
    final_mono = Image.alpha_composite(final_mono, Image.fromarray(edge_rgba))
    
    return final_mono

def render_nniirt_3d(size=260):
    # Load authentic nniirt icon
    src = Image.open("smm/media/nniirt_icon.png").convert("RGBA")
    
    # Resize src
    src = src.resize((size, size), Image.Resampling.LANCZOS)
    arr = np.array(src)
    
    # White radar arcs are where pixels are bright
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    brightness = (r.astype(float) + g.astype(float) + b.astype(float)) / 3.0
    
    # Extract radar lines
    radar_mask = (brightness > 130) & (a > 100)
    mask_im = Image.fromarray((radar_mask * 255).astype(np.uint8))
    
    # Create 3D metallic relief for the radar arcs
    # Base: bright steel (180, 210, 235), Highlight: pure white cyan (220, 245, 255), Shadow: (20, 45, 70)
    line_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    line_img.putalpha(mask_im)
    
    relief = create_metallic_relief(line_img, base_color=(160, 200, 235), highlight_color=(235, 250, 255), shadow_color=(15, 35, 60), depth=2)
    
    # Add cyan electric glow
    edge = mask_im.filter(ImageFilter.GaussianBlur(4))
    glow_arr = np.array(edge)
    glow_rgba = np.zeros((size, size, 4), dtype=np.uint8)
    glow_rgba[:,:,0] = 0
    glow_rgba[:,:,1] = 200
    glow_rgba[:,:,2] = 255
    glow_rgba[:,:,3] = (glow_arr * 0.7).astype(np.uint8)
    glow_layer = Image.fromarray(glow_rgba)
    
    res = Image.alpha_composite(glow_layer, relief)
    return res

def render_ngpu_3d(size=250):
    src = Image.open("img/shields/ngpu_minina.png").convert("RGBA")
    src = src.resize((size, size), Image.Resampling.LANCZOS)
    arr = np.array(src)
    
    # In ngpu_minina.png: dark pixels are the seal lines
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
    brightness = (r.astype(float) + g.astype(float) + b.astype(float)) / 3.0
    
    # Invert so seal lines are positive mask
    seal_mask = (brightness < 170)
    mask_im = Image.fromarray((seal_mask * 255).astype(np.uint8))
    
    # Smooth edges
    mask_im = mask_im.filter(ImageFilter.GaussianBlur(1))
    mask_im = mask_im.point(lambda p: 255 if p > 100 else (p * 2.5))
    
    line_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    line_img.putalpha(mask_im)
    
    # 3D burnished gold relief
    # Base gold: (212, 175, 55), Highlight: (255, 235, 150), Shadow: (70, 40, 10)
    relief = create_metallic_relief(line_img, base_color=(212, 175, 55), highlight_color=(255, 240, 170), shadow_color=(70, 35, 10), depth=3)
    
    # Golden glow
    edge = mask_im.filter(ImageFilter.GaussianBlur(3))
    glow_arr = np.array(edge)
    glow_rgba = np.zeros((size, size, 4), dtype=np.uint8)
    glow_rgba[:,:,0] = 255
    glow_rgba[:,:,1] = 215
    glow_rgba[:,:,2] = 0
    glow_rgba[:,:,3] = (glow_arr * 0.6).astype(np.uint8)
    glow_layer = Image.fromarray(glow_rgba)
    
    res = Image.alpha_composite(glow_layer, relief)
    return res

print("3D Renderers configured")

