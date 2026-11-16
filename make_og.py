#!/usr/bin/env python3
"""og.png 1200x630 — Jack's Diner (2x supersample).
Late-night diner sign: espresso ground, gold neon glow on the wordmark, cherry
rule, gold checkerboard foot. Shop identity only — no builder markers."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
S = 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

INK = (23, 19, 16); PANEL = (36, 27, 17)
CREAM = (244, 233, 211); GOLD = (227, 168, 62); RED = (207, 46, 51)
DIM = (195, 177, 147)

def font(paths, size, index=0):
    bases = ["/System/Library/Fonts/", "/System/Library/Fonts/Supplemental/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size, index)
                except Exception: pass
    return ImageFont.load_default()

sign  = lambda s: font(["Futura.ttc", "Trebuchet MS Bold.ttf"], s * S)
serif = lambda s: font(["Georgia Bold.ttf", "Times New Roman Bold.ttf"], s * S)
serifm = lambda s: font(["Georgia.ttf", "Times New Roman.ttf"], s * S)

img = Image.new("RGB", (W * S, H * S), INK)
d = ImageDraw.Draw(img)

# warm vignette from top-right, like a signlit window
glow = Image.new("RGB", (W * S, H * S), INK)
gd = ImageDraw.Draw(glow)
gd.ellipse((-W * 0.3 * S, -H * 1.1 * S, W * 1.3 * S, H * 0.6 * S), fill=PANEL)
img = Image.blend(img, glow, 0.55)
d = ImageDraw.Draw(img)

def center_text(dr, xy_y, f, text, fill, ls=0, glow_layers=None, glow_color=None, anchor="mm"):
    x = W * S // 2
    if ls:
        widths = [dr.textbbox((0, 0), ch, font=f)[2] for ch in text]
        total = sum(widths) + ls * S * (len(text) - 1)
        cx = x - total / 2
        for ch, cw in zip(text, widths):
            dr.text((cx + cw / 2, xy_y * S), ch, font=f, fill=fill, anchor="mm")
            cx += cw + ls * S
    else:
        dr.text((x, xy_y * S), text, font=f, fill=fill, anchor=anchor)

# plate + fork icon above the wordmark
cx, cy = W * S // 2, 118 * S
d.ellipse((cx - 44 * S, cy - 44 * S, cx + 44 * S, cy + 44 * S), outline=GOLD, width=3 * S)
d.ellipse((cx - 30 * S, cy - 30 * S, cx + 30 * S, cy + 30 * S), outline=(244, 233, 211), width=2 * S)
d.rounded_rectangle((cx - 5 * S, cy - 24 * S, cx + 5 * S, cy + 24 * S), radius=5 * S, fill=RED)
d.rectangle((cx - 20 * S, cy - 24 * S, cx - 16 * S, cy - 4 * S), fill=CREAM)
d.rectangle((cx + 16 * S, cy - 24 * S, cx + 20 * S, cy - 4 * S), fill=CREAM)
d.rectangle((cx - 20 * S, cy - 8 * S, cx + 20 * S, cy - 4 * S), fill=CREAM)

# neon glow behind wordmark: blurred passes
gl = Image.new("RGBA", img.size, (0, 0, 0, 0))
gd = ImageDraw.Draw(gl)
f_word = sign(84)
gd.text((W * S // 2, 250 * S), "JACK\u2019S DINER", font=f_word, fill=GOLD + (255,), anchor="mm")
from PIL import ImageFilter
halo = gl.filter(ImageFilter.GaussianBlur(18 * S // 2))
img.paste(halo, (0, 0), halo)
img.paste(halo, (0, 0), halo)
d = ImageDraw.Draw(img)
center_text(d, 250, f_word, "JACK\u2019S DINER", CREAM, ls=6)

center_text(d, 340, sign(26), "CHARLESTON\u2019S ONLY LEGENDARY DINER", GOLD, ls=8)

# cherry rule
d.rectangle((W // 2 * S - 150 * S, 382 * S, W // 2 * S + 150 * S, 386 * S), fill=RED)

center_text(d, 440, serif(30), "Breakfast all day \u00b7 Gravy three ways", CREAM)
center_text(d, 500, serifm(22), "Open daily 7:30 a.m.\u20139 p.m. \u00b7 41B George St, Charleston SC", DIM)

# checkerboard foot band
cell = 24 * S
for i in range(0, (W * S) // cell + 1):
    if i % 2 == 0:
        d.rectangle((i * cell, H * S - cell, (i + 1) * cell, H * S), fill=GOLD)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT))
