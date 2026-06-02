#!/usr/bin/env python3
"""
Génère 30 logos PNG fictifs pour OpenScanR.
Chaque logo est unique : forme, couleur, initiales et style différents.
Convention : logo_<slug>.png
"""
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(__file__).parent
SIZE = (400, 200)  # largeur x hauteur en pixels

# ---------------------------------------------------------------------------
# Données des 30 sociétés fictives
# ---------------------------------------------------------------------------
COMPANIES = [
    ("acme",         "ACME",         "AC", (0.10, 0.28, 0.58)),
    ("nova",         "NOVA",         "NV", (0.70, 0.12, 0.12)),
    ("zephyr",       "ZEPHYR",       "ZP", (0.08, 0.47, 0.28)),
    ("orbit",        "ORBIT",        "OR", (0.40, 0.20, 0.60)),
    ("peak",         "PEAK",         "PK", (0.80, 0.45, 0.00)),
    ("lumia",        "LUMIA",        "LU", (0.00, 0.55, 0.65)),
    ("forge",        "FORGE",        "FG", (0.50, 0.25, 0.10)),
    ("stratos",      "STRATOS",      "ST", (0.15, 0.35, 0.65)),
    ("helix",        "HELIX",        "HX", (0.60, 0.05, 0.40)),
    ("axion",        "AXION",        "AX", (0.00, 0.40, 0.30)),
    ("crest",        "CREST",        "CR", (0.75, 0.20, 0.10)),
    ("delta",        "DELTA",        "DL", (0.20, 0.20, 0.60)),
    ("echo",         "ECHO",         "EC", (0.00, 0.60, 0.50)),
    ("fulcrum",      "FULCRUM",      "FC", (0.55, 0.35, 0.00)),
    ("glyph",        "GLYPH",        "GL", (0.30, 0.10, 0.55)),
    ("hydra",        "HYDRA",        "HD", (0.05, 0.45, 0.55)),
    ("ionic",        "IONIC",        "IO", (0.65, 0.15, 0.25)),
    ("jetstream",    "JETSTREAM",    "JS", (0.10, 0.50, 0.20)),
    ("kore",         "KORE",         "KR", (0.45, 0.00, 0.35)),
    ("lumen",        "LUMEN",        "LM", (0.80, 0.60, 0.00)),
    ("mantra",       "MANTRA",       "MN", (0.20, 0.40, 0.60)),
    ("nexum",        "NEXUM",        "NX", (0.60, 0.20, 0.40)),
    ("onyx",         "ONYX",         "ON", (0.15, 0.15, 0.15)),
    ("prism",        "PRISM",        "PR", (0.00, 0.35, 0.70)),
    ("quark",        "QUARK",        "QK", (0.70, 0.35, 0.00)),
    ("radix",        "RADIX",        "RX", (0.40, 0.60, 0.10)),
    ("synapse",      "SYNAPSE",      "SY", (0.55, 0.00, 0.55)),
    ("terra",        "TERRA",        "TR", (0.35, 0.55, 0.15)),
    ("ultra",        "ULTRA",        "UL", (0.00, 0.25, 0.75)),
    ("vortex",       "VORTEX",       "VX", (0.65, 0.10, 0.10)),
]

# ---------------------------------------------------------------------------
# Helpers couleurs
# ---------------------------------------------------------------------------
def rgb01_to_255(r, g, b):
    return (int(r * 255), int(g * 255), int(b * 255))

def lighten(r, g, b, factor=0.6):
    return (r + (1 - r) * factor, g + (1 - g) * factor, b + (1 - b) * factor)

def darken(r, g, b, factor=0.4):
    return (r * (1 - factor), g * (1 - factor), b * (1 - factor))

def hex_color(r, g, b):
    return rgb01_to_255(r, g, b)

# ---------------------------------------------------------------------------
# 6 styles de formes
# ---------------------------------------------------------------------------

def shape_circle_badge(draw, w, h, color, light, dark):
    """Cercle plein avec bordure."""
    cx, cy, r = w // 4, h // 2, h // 2 - 10
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hex_color(*color), outline=hex_color(*dark), width=4)


def shape_rounded_rect(draw, w, h, color, light, dark):
    """Rectangle arrondi."""
    pad = 10
    draw.rounded_rectangle([pad, pad, w // 2 - pad, h - pad], radius=30,
                            fill=hex_color(*color), outline=hex_color(*dark), width=3)


def shape_hexagon(draw, w, h, color, light, dark):
    """Hexagone régulier."""
    cx, cy = w // 4, h // 2
    r = h // 2 - 10
    pts = [
        (cx + r * math.cos(math.radians(60 * i - 30)),
         cy + r * math.sin(math.radians(60 * i - 30)))
        for i in range(6)
    ]
    draw.polygon(pts, fill=hex_color(*color), outline=hex_color(*dark), width=3)


def shape_diamond(draw, w, h, color, light, dark):
    """Losange."""
    cx, cy = w // 4, h // 2
    rx, ry = w // 5, h // 2 - 10
    pts = [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]
    draw.polygon(pts, fill=hex_color(*color), outline=hex_color(*dark), width=3)


def shape_shield(draw, w, h, color, light, dark):
    """Bouclier (pentagone inversé)."""
    cx, cy = w // 4, h // 2
    rx, ry = w // 5, h // 2 - 8
    pts = [
        (cx - rx, cy - ry),
        (cx + rx, cy - ry),
        (cx + rx, cy),
        (cx, cy + ry),
        (cx - rx, cy),
    ]
    draw.polygon(pts, fill=hex_color(*color), outline=hex_color(*dark), width=3)


def shape_star(draw, w, h, color, light, dark):
    """Étoile à 5 branches."""
    cx, cy = w // 4, h // 2
    r_outer = h // 2 - 10
    r_inner = r_outer // 2
    pts = []
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=hex_color(*color), outline=hex_color(*dark), width=2)


SHAPES = [shape_circle_badge, shape_rounded_rect, shape_hexagon,
          shape_diamond, shape_shield, shape_star]

# ---------------------------------------------------------------------------
# 5 styles de mise en page texte
# ---------------------------------------------------------------------------

def layout_name_right(draw, name, initials, w, h, color, light, font_lg, font_sm):
    """Nom de la société à droite de la forme."""
    x_text = w // 2 + 10
    # Nom principal
    bbox = draw.textbbox((0, 0), name, font=font_lg)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x_text, (h - th) // 2), name,
              fill=hex_color(*color), font=font_lg)


def layout_name_below(draw, name, initials, w, h, color, light, font_lg, font_sm):
    """Nom sous la forme."""
    bbox = draw.textbbox((0, 0), name, font=font_sm)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, h - 42), name,
              fill=hex_color(*color), font=font_sm)


def layout_initials_only(draw, name, initials, w, h, color, light, font_lg, font_sm):
    """Initiales larges centrées dans la moitié droite."""
    bbox = draw.textbbox((0, 0), initials, font=font_lg)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((w // 2 + (w // 2 - tw) // 2, (h - th) // 2), initials,
              fill=hex_color(*color), font=font_lg)


def layout_stacked(draw, name, initials, w, h, color, light, font_lg, font_sm):
    """Initiales + nom empilés verticalement."""
    x = w // 2 + 10
    bbox_i = draw.textbbox((0, 0), initials, font=font_lg)
    ih = bbox_i[3] - bbox_i[1]
    bbox_n = draw.textbbox((0, 0), name, font=font_sm)
    nh = bbox_n[3] - bbox_n[1]
    total = ih + 6 + nh
    y = (h - total) // 2
    draw.text((x, y), initials, fill=hex_color(*color), font=font_lg)
    draw.text((x, y + ih + 6), name, fill=hex_color(*light), font=font_sm)


def layout_tagline(draw, name, initials, w, h, color, light, font_lg, font_sm):
    """Nom + sous-titre 'Solutions & Services'."""
    x = w // 2 + 10
    bbox = draw.textbbox((0, 0), name, font=font_sm)
    nw, nh = bbox[2] - bbox[0], bbox[3] - bbox[1]
    sub = "Solutions & Services"
    bbox2 = draw.textbbox((0, 0), sub, font=font_sm)
    sh = bbox2[3] - bbox2[1]
    total = nh + 8 + sh
    y = (h - total) // 2
    draw.text((x, y), name, fill=hex_color(*color), font=font_sm)
    draw.text((x, y + nh + 8), sub, fill=hex_color(*light), font=font_sm)


LAYOUTS = [layout_name_right, layout_name_below, layout_initials_only,
           layout_stacked, layout_tagline]

# ---------------------------------------------------------------------------
# 6 styles de fond
# ---------------------------------------------------------------------------

def bg_white(img, draw, w, h, color, light):
    img.paste(hex_color(1, 1, 1) + (255,), [0, 0, w, h])  # blanc


def bg_light(img, draw, w, h, color, light):
    c = hex_color(*light)
    draw.rectangle([0, 0, w, h], fill=c + (255,) if len(c) == 3 else c)


def bg_dark(img, draw, w, h, color, light):
    dark = darken(*color, factor=0.7)
    draw.rectangle([0, 0, w, h], fill=hex_color(*dark))


def bg_gradient_h(img, draw, w, h, color, light):
    for x in range(w):
        t = x / w
        r = int((color[0] * (1 - t) + light[0] * t) * 255)
        g = int((color[1] * (1 - t) + light[1] * t) * 255)
        b = int((color[2] * (1 - t) + light[2] * t) * 255)
        draw.line([(x, 0), (x, h)], fill=(r, g, b))


def bg_gradient_v(img, draw, w, h, color, light):
    for y in range(h):
        t = y / h
        r = int((color[0] * (1 - t) + 1.0 * t) * 255)
        g = int((color[1] * (1 - t) + 1.0 * t) * 255)
        b = int((color[2] * (1 - t) + 1.0 * t) * 255)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def bg_split(img, draw, w, h, color, light):
    draw.rectangle([0, 0, w // 2, h], fill=hex_color(*color))
    draw.rectangle([w // 2, 0, w, h], fill=(255, 255, 255))


BACKGROUNDS = [bg_white, bg_light, bg_dark, bg_gradient_h, bg_gradient_v, bg_split]

# ---------------------------------------------------------------------------
# Couleur du texte selon le fond
# ---------------------------------------------------------------------------

def text_color_for_bg(bg_idx, color, light):
    if bg_idx == 2:   # fond sombre → texte clair
        return lighten(*color, factor=0.9)
    if bg_idx == 0:   # fond blanc → couleur primaire
        return color
    return darken(*color, factor=0.3)

# ---------------------------------------------------------------------------
# Génération
# ---------------------------------------------------------------------------

def load_font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_logo(slug, name, initials, color_01, index, output_dir):
    w, h = SIZE
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    light = lighten(*color_01, factor=0.55)
    dark = darken(*color_01, factor=0.3)

    bg_idx = index % len(BACKGROUNDS)
    BACKGROUNDS[bg_idx](img, draw, w, h, color_01, light)

    # Détermine la couleur du texte selon le fond
    txt_color = text_color_for_bg(bg_idx, color_01, light)
    # Sur fond split (bg_idx==5), la forme est sur fond couleur,
    # le texte est à droite sur fond blanc → forcer la couleur primaire
    if bg_idx == 5:
        txt_color = color_01

    shape_idx = index % len(SHAPES)
    SHAPES[shape_idx](draw, w, h, color_01, light, dark)

    # Initiales dans la forme
    font_init = load_font(56)
    bbox = draw.textbbox((0, 0), initials, font=font_init)
    iw, ih = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx = w // 4
    draw.text((cx - iw // 2, h // 2 - ih // 2), initials,
              fill=(255, 255, 255), font=font_init)

    # Texte layout
    font_lg = load_font(40)
    font_sm = load_font(26)
    layout_idx = index % len(LAYOUTS)
    LAYOUTS[layout_idx](draw, name, initials, w, h, txt_color, light, font_lg, font_sm)

    # Sauvegarde
    out_path = output_dir / f"logo_{slug}.png"
    img.convert("RGB").save(str(out_path), "PNG")
    return out_path


def main():
    output_dir = Path(__file__).parent
    print(f"Génération de {len(COMPANIES)} logos dans : {output_dir}\n")
    for i, (slug, name, initials, color) in enumerate(COMPANIES):
        path = generate_logo(slug, name, initials, color, i, output_dir)
        print(f"  [{i+1:02d}/{len(COMPANIES)}] {path.name}")
    print(f"\n✓ {len(COMPANIES)} logos générés.")


if __name__ == "__main__":
    main()
