import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter, ImageFont

# Load image and rotate upright
orig_img = Image.open('Lectures/TransmissionLine/images/IMG_2205.jpg')
upright = ImageOps.exif_transpose(orig_img)
w, h = upright.size # 3024 x 4032

# Edge map for local subpixel refinement
edge_img = Image.open('/Users/bcornelusse/.gemini/antigravity/brain/30a10181-4a86-4cf1-ad9f-d6efaa2cedae/scratch/full_edges.jpg')
arr = np.array(edge_img, dtype=float)

def refine_point(pt, search_r=8):
    x, y = pt
    ix = int(round(x))
    iy = int(round(y))
    if ix < 0 or ix >= w or iy < 0 or iy >= h:
        return pt
    y_min = max(0, iy - search_r)
    y_max = min(h, iy + search_r + 1)
    col = arr[y_min:y_max, ix]
    if len(col) == 0: return pt
    best_off = np.argmax(col)
    val = col[best_off]
    if val > 90:
        if 0 < best_off < len(col) - 1:
            v0, v1, v2 = col[best_off-1], col[best_off], col[best_off+1]
            denom = v0 - 2*v1 + v2
            sub = 0.5 * (v0 - v2) / denom if abs(denom) > 1e-4 else 0.0
        else:
            sub = 0.0
        return (x, y_min + best_off + sub)
    return pt

# Spline interpolation through control points
def catmull_rom_spline(pts, num_samples=500):
    """Generates a smooth Catmull-Rom spline passing exactly through pts."""
    pts = np.array(pts)
    n = len(pts)
    if n < 2: return pts
    if n == 2:
        return np.column_stack([np.linspace(pts[0, 0], pts[1, 0], num_samples),
                                np.linspace(pts[0, 1], pts[1, 1], num_samples)])
    
    # Duplicate endpoints for phantom control points
    p_ext = np.vstack([pts[0] - (pts[1] - pts[0]), pts, pts[-1] + (pts[-1] - pts[-2])])
    
    curve = []
    samples_per_seg = max(5, num_samples // (n - 1))
    t = np.linspace(0, 1, samples_per_seg)
    t2 = t * t
    t3 = t2 * t
    
    for i in range(1, n):
        p0, p1, p2, p3 = p_ext[i-1], p_ext[i], p_ext[i+1], p_ext[i+2]
        # Catmull-Rom basis:
        # q(t) = 0.5 * ((2*p1) + (-p0 + p2)*t + (2*p0 - 5*p1 + 4*p2 - p3)*t^2 + (-p0 + 3*p1 - 3*p2 + p3)*t^3)
        seg = 0.5 * (
            np.outer(2 * np.ones_like(t), p1) +
            np.outer(t, -p0 + p2) +
            np.outer(t2, 2*p0 - 5*p1 + 4*p2 - p3) +
            np.outer(t3, -p0 + 3*p1 - 3*p2 + p3)
        )
        curve.append(seg[:-1] if i < n - 1 else seg)
        
    return np.vstack(curve)

# Define the 7 wires with control points that pass through the clamps and sky
wires_config = [
    # Ground / Shield Wire (Apex)
    {
        'name': 'Ground / Shield Wire',
        'phase': 'Ground',
        'color': (255, 255, 255), # Pure White
        'halo': (0, 0, 0, 200),
        'width': 8,
        'points': [
            (500, 72), (900, 190), (1300, 290), (1680, 360),
            (1950, 630), (2200, 880), (2500, 1180), (2800, 1480), (3023, 1700)
        ]
    },
    # Circuit 1 - Phase A (Top Right, Red)
    {
        'name': 'Circuit 1 - Phase A (L1)',
        'phase': 'Phase A',
        'color': (255, 45, 45), # Vibrant Crimson-Red
        'halo': (0, 0, 0, 200),
        'width': 11,
        'points': [
            (1180, 0), (1420, 235), (1660, 480), (1915, 735),
            (2150, 975), (2400, 1234), (2650, 1490), (2900, 1746), (3023, 1873)
        ]
    },
    # Circuit 1 - Phase B (Inner Right, Amber-Gold)
    {
        'name': 'Circuit 1 - Phase B (L2)',
        'phase': 'Phase B',
        'color': (255, 205, 0), # Vibrant Amber-Gold
        'halo': (0, 0, 0, 200),
        'width': 11,
        'points': [
            (862, 0), (1120, 260), (1380, 530), (1680, 840),
            (1950, 1080), (2200, 1315), (2500, 1590), (2800, 1860), (3023, 2040)
        ]
    },
    # Circuit 1 - Phase C (Middle Right, Blue)
    {
        'name': 'Circuit 1 - Phase C (L3)',
        'phase': 'Phase C',
        'color': (0, 160, 255), # Vibrant Electric Blue
        'halo': (0, 0, 0, 200),
        'width': 11,
        'points': [
            (0, 750), (450, 910), (900, 1060), (1350, 1220), (1775, 1400),
            (2050, 1630), (2350, 1870), (2650, 2080), (2900, 2220), (3023, 2275)
        ]
    },
    # Circuit 2 - Phase A (Top Left, Red)
    {
        'name': 'Circuit 2 - Phase A (L1)',
        'phase': 'Phase A',
        'color': (255, 45, 45), # Vibrant Crimson-Red
        'halo': (0, 0, 0, 200),
        'width': 11,
        'points': [
            (0, 500), (350, 600), (700, 710), (1050, 820), (1420, 930),
            (1750, 1180), (2100, 1440), (2450, 1680), (2750, 1880), (3023, 2020)
        ]
    },
    # Circuit 2 - Phase B (Middle Left, Amber-Gold)
    {
        'name': 'Circuit 2 - Phase B (L2)',
        'phase': 'Phase B',
        'color': (255, 205, 0), # Vibrant Amber-Gold
        'halo': (0, 0, 0, 200),
        'width': 11,
        'points': [
            (0, 1051), (250, 1120), (550, 1235), (850, 1350), (1150, 1455), (1290, 1500),
            (1600, 1690), (1950, 1890), (2300, 2085), (2650, 2260), (3023, 2410)
        ]
    },
    # Circuit 2 - Phase C (Bottom Left, Blue)
    {
        'name': 'Circuit 2 - Phase C (L3)',
        'phase': 'Phase C',
        'color': (0, 160, 255), # Vibrant Electric Blue
        'halo': (0, 0, 0, 200),
        'width': 11,
        'points': [
            (0, 1285), (250, 1345), (550, 1435), (850, 1520), (1150, 1605), (1335, 1645),
            (1650, 1785), (2000, 1980), (2350, 2180), (2700, 2355), (3023, 2480)
        ]
    }
]

print("Script template ready")

def render_image(add_legend=False):
    halo_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_halo = ImageDraw.Draw(halo_layer)
    
    wire_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw_wire = ImageDraw.Draw(wire_layer)
    
    for wire in wires_config:
        # Refine points
        refined = [refine_point(p) for p in wire['points']]
        # Generate smooth curve
        curve = catmull_rom_spline(refined, num_samples=800)
        curve_pts = [tuple(p) for p in curve]
        
        col = wire['color']
        halo_col = wire['halo']
        width = wire['width']
        
        # Draw halo
        draw_halo.line(curve_pts, fill=halo_col, width=width + 8, joint='round')
        # Draw wire
        draw_wire.line(curve_pts, fill=col + (255,), width=width, joint='round')
        
    halo_blurred = halo_layer.filter(ImageFilter.GaussianBlur(radius=2))
    
    comp = upright.convert('RGBA')
    comp = Image.alpha_composite(comp, halo_blurred)
    comp = Image.alpha_composite(comp, wire_layer)
    
    if add_legend:
        # Subtle, clean legend box in top-left
        card_w, card_h = 1000, 290
        card = Image.new('RGBA', (card_w, card_h), (15, 23, 42, 215)) # Dark slate semi-transparent
        draw_card = ImageDraw.Draw(card)
        draw_card.rounded_rectangle([(0, 0), (card_w-1, card_h-1)], radius=24, outline=(255, 255, 255, 140), width=3)
        
        try:
            font_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 40)
            font_item = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 36)
            font_sub = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
        except Exception:
            font_title = font_item = font_sub = ImageFont.load_default()
            
        draw_card.text((36, 22), "Overhead Line Phase Identification", fill=(255, 255, 255), font=font_title)
        draw_card.text((36, 72), "Double-Circuit 3-Phase Transmission Line (SwissGrid)", fill=(190, 205, 225), font=font_sub)
        
        items = [
            ("Phase A (L1)", (255, 45, 45)),
            ("Phase B (L2)", (255, 205, 0)),
            ("Phase C (L3)", (0, 160, 255)),
            ("Ground / Shield", (255, 255, 255)),
        ]
        
        coords = [
            (36, 128), (500, 128),
            (36, 198), (500, 198)
        ]
        
        for (label, col), (ix, iy) in zip(items, coords):
            draw_card.rounded_rectangle([(ix, iy + 6), (ix + 55, iy + 26)], radius=6, fill=col, outline=(0, 0, 0, 160), width=2)
            draw_card.text((ix + 70, iy), label, fill=(255, 255, 255), font=font_item)
            
        comp.paste(card, (80, 80), card)
        
    return comp.convert('RGB')

# Generate test outputs
res_clean = render_image(add_legend=False)
res_clean.resize((1512, 2016), Image.Resampling.LANCZOS).save('/Users/bcornelusse/.gemini/antigravity/brain/30a10181-4a86-4cf1-ad9f-d6efaa2cedae/scratch/spline_clean.jpg', quality=90)

res_legend = render_image(add_legend=True)
res_legend.resize((1512, 2016), Image.Resampling.LANCZOS).save('/Users/bcornelusse/.gemini/antigravity/brain/30a10181-4a86-4cf1-ad9f-d6efaa2cedae/scratch/spline_legend.jpg', quality=90)

print("Spline previews rendered!")
