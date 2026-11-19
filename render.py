#!/usr/bin/env python3
"""Render news.png: one-page front page of world news, Thu 19 Nov 2026.
Fresh build for make.fun news-image-20261119. Stdlib + Pillow only.
Deterministic: fixed fonts, colours, layout; no time, no randomness."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")

PAPER = (247, 243, 234)
INK = (18, 28, 48)
RED = (178, 34, 22)
BLUE = (29, 78, 216)
TEAL = (13, 110, 105)
GOLD = (176, 124, 18)
CARD = (255, 255, 255)
LINE = (18, 28, 48)
SOFT = (90, 98, 118)
MAP_BG = (214, 232, 240)
LAND = (168, 196, 168)
SEA_DOT = (178, 34, 22)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 52)
F_KICK = font("DejaVuSans-Bold.ttf", 15)
F_SUB = font("DejaVuSans.ttf", 14)
F_HERO_H = font("DejaVuSans-Bold.ttf", 16)
F_HERO_S = font("DejaVuSans.ttf", 12)
F_CARD_H = font("DejaVuSans-Bold.ttf", 14)
F_CARD_S = font("DejaVuSans.ttf", 11)
F_SEC = font("DejaVuSans-Bold.ttf", 15)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_BRIEF_N = font("DejaVuSans-Bold.ttf", 12)
F_SMALL = font("DejaVuSans.ttf", 11)
F_SMALL_B = font("DejaVuSans-Bold.ttf", 11)
F_MAP_L = font("DejaVuSans-Bold.ttf", 10)
F_FOOT = font("DejaVuSans.ttf", 10)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, f, width, fill=INK, leading=None):
    lh = leading or int(f.size * 1.25)
    for ln in wrap(d, text, f, width):
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def icon(d, kind, cx, cy, r, col):
    """Tiny flat pictogram drawn with primitives, one per story."""
    if kind == "summit":  # three heads at a table
        for dx in (-r, 0, r):
            d.ellipse([cx + dx - r // 2, cy - r, cx + dx + r // 2, cy], fill=col)
        d.rectangle([cx - r * 2, cy + r // 3, cx + r * 2, cy + r // 3 + 5], fill=col)
    elif kind == "gavel":
        d.rectangle([cx - r, cy - r // 2, cx + r // 2, cy], fill=col)
        d.line([cx + r // 2, cy - r // 2, cx + r, cy + r], fill=col, width=4)
        d.rectangle([cx - r, cy + r // 2, cx + r, cy + r // 2 + 5], fill=col)
    elif kind == "chart":
        for i, h in enumerate((0.4, 0.8, 0.55, 1.0)):
            x0 = cx - r + i * (r // 2)
            d.rectangle([x0, cy + r - h * r, x0 + r // 3, cy + r], fill=col)
        d.line([cx - r, cy + r, cx + r, cy - r], fill=RED, width=3)
    elif kind == "game":
        d.rounded_rectangle([cx - r, cy - r // 2, cx + r, cy + r // 2], radius=8, fill=col)
        d.ellipse([cx - r // 2, cy - 3, cx - r // 2 + 6, cy + 3], fill=PAPER)
        d.ellipse([cx + r // 2 - 6, cy - 3, cx + r // 2, cy + 3], fill=PAPER)
    elif kind == "bridge":
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=col, width=4)
        d.line([cx - r, cy + 2, cx + r, cy + 2], fill=col, width=4)
        d.line([cx, cy - r, cx, cy], fill=col, width=3)
    elif kind == "missile":
        d.polygon([(cx, cy - r), (cx + r // 2, cy + r // 2), (cx - r // 2, cy + r // 2)],
                  fill=col)
        d.line([cx - r // 2, cy + r // 2, cx - r, cy + r], fill=col, width=3)
        d.line([cx + r // 2, cy + r // 2, cx + r, cy + r], fill=col, width=3)
    elif kind == "globe":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
        d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=col, width=2)
        d.line([cx - r, cy, cx + r, cy], fill=col, width=2)
    elif kind == "flame":
        d.polygon([(cx, cy - r), (cx + r // 2, cy), (cx + r // 3, cy + r),
                   (cx - r // 3, cy + r), (cx - r // 2, cy)], fill=col)
    elif kind == "handshake":
        d.rectangle([cx - r, cy - r // 3, cx - r // 4, cy + r // 3], fill=col)
        d.rectangle([cx + r // 4, cy - r // 3, cx + r, cy + r // 3], fill=col)
        d.polygon([(cx - r // 4, cy - r // 3), (cx + r // 4, cy - r // 3),
                   (cx, cy + r // 2)], fill=col)
    elif kind == "euro":
        d.text((cx - r // 2, cy - r), "\u20ac", font=font("DejaVuSans-Bold.ttf", 2 * r),
               fill=col)
    elif kind == "frame":
        d.rectangle([cx - r, cy - r // 2, cx + r, cy + r // 2], outline=col, width=4)
        d.ellipse([cx - r // 2, cy - r // 4, cx, cy + r // 4], fill=GOLD)
    elif kind == "sat":
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2], fill=col)
        d.rectangle([cx - r, cy - 3, cx - r // 2, cy + 3], fill=col)
        d.rectangle([cx + r // 2, cy - 3, cx + r, cy + 3], fill=col)


# (num, kind, colour, headline, sub-line, map x, map y)
HERO = [
    (1, "summit", RED, "Trump, Xi & Putin meet in Shenzhen",
     "First three-way summit of the three nuclear powers, on APEC sidelines.", 860, 120),
    (2, "gavel", BLUE, "World court rules on Rohingya genocide",
     "ICJ finds Myanmar guilty of genocide, 9-6, The Hague.", 480, 70),
    (3, "chart", TEAL, "Anthropic IPO: $81.3bn, a record",
     "Claude maker priced at $83 a share; $1.5tn valuation, biggest debut ever.", 210, 110),
    (4, "game", GOLD, "GTA VI launches worldwide",
     "Rockstar's game arrives after a 13-year wait; midnight queues round the globe.", 150, 150),
]

DRAWN = [
    (5, "bridge", RED, "Ukraine strikes Crimean Bridge again",
     "Road traffic halted after a new missile hit; second night of strikes.", 590, 85),
    (6, "missile", RED, "Iran attacks Gulf states",
     "Kuwait repels its first Iranian attack in two months; Bahrain also hit.", 620, 140),
    (7, "globe", TEAL, "COP31 talks stuck in Antalya",
     "Ministers meet late to unblock a final climate text as deadline nears.", 545, 140),
    (8, "flame", RED, "Bangladesh in turmoil",
     "Yunus's ancestral home set on fire; violence in 28 districts in 10 days.", 740, 150),
    (9, "handshake", BLUE, "US & Venezuela sign military pact",
     "Pentagon chief Hegseth in Caracas, first such visit since Maduro's capture.", 215, 230),
    (10, "euro", BLUE, "EU proposes \u20ac45bn loan for Ukraine",
     "Von der Leyen's new loan for 2027, on top of \u20ac90bn already planned.", 520, 90),
    (11, "frame", GOLD, "Van Gogh sells for $190.4m",
     "Sotheby's New York: a record price for the artist, for an 1890 canvas.", 250, 145),
    (12, "sat", TEAL, "Voyager 1: one light-day out",
     "NASA's 1977 probe is now a full light-day from Earth, still sending data.", 960, 30),
]

BRIEFS = [
    "IAEA: N. Korea expanded uranium enrichment.",
    "Israel ground op beyond Gaza's Yellow Line.",
    "Ethiopia & Eritrea mass troops at border.",
    "589m children lived in conflict zones in 2025.",
    "Fiji & Tonga declare drought emergencies.",
    "Indonesia fires burned nearly 3m hectares.",
    "Indonesia passes asset-forfeiture law.",
    "S. Korea exports pass $1tn, a first.",
    "S. Korea exam held under AI-cheating curbs.",
    "IMF: world public debt nears 100% of GDP.",
    "IMF deal unlocks $2.3bn for Egypt.",
    "Markets slide: Hang Seng \u22121.9%, Brent $89.59.",
    "Trump hints at Blackwell chip sales to China.",
    "Nvidia board rejects Huang's return as CEO.",
    "US loses measles elimination status.",
    "Ebola strain vaccines trialled in DR Congo.",
    "Webb confirms rare supergiant star merger.",
    "Antarctic blue whales up 10x since whaling.",
    "Waymo pulls driverless taxis off freeways.",
    "Cyclone Aqwan heads for India's east coast.",
    "Record atmospheric-river rain hits California.",
    "Democrats win Alaska, take 56-seat Senate.",
    "Jeffries picked as Speaker nominee, a first.",
    "Pastor convicted over Haiti president's killing.",
    "Imamoglu + 8 sentenced in Turkey CHP case.",
    "Five EU nations plan Rwanda asylum transfers.",
    "Alcaraz beats Medvedev at ATP Finals.",
    "Chelsea beat PSG 1\u20130, Women's Champions League.",
    "England win ODI series in Australia.",
    "Buffalo beat Central Michigan 40-21.",
]

# Rough continent blobs for the map, in a 1000x400 virtual space.
# Map inner area is 632 wide x 146 tall, starting below the map title.
LANDS = [
    (40, 60, 180, 110),    # North America
    (180, 200, 90, 130),   # South America
    (470, 50, 80, 80),     # Europe
    (480, 150, 90, 140),   # Africa
    (600, 40, 320, 140),   # Asia
    (760, 200, 110, 50),   # SE Asia / Indonesia
    (830, 270, 80, 60),    # Australia
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG, outline=LINE, width=2)
    d.text((x0 + 10, y0 + 6), "WHERE IT HAPPENED  \u2014  THE WORLD, 19 NOVEMBER 2026",
           font=F_MAP_L, fill=INK)
    sx, sy = x0, y0 + 22
    for (lx, ly, lw, lh) in LANDS:
        d.rounded_rectangle([sx + lx * w // 1000, sy + ly * (h - 22) // 400,
                             sx + (lx + lw) * w // 1000, sy + (ly + lh) * (h - 22) // 400],
                            radius=12, fill=LAND)
    for (num, kind, col, head, sub, mx, my) in HERO + DRAWN:
        px, py = sx + mx * w // 1000, sy + my * (h - 22) // 400
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=SEA_DOT, outline=(255, 255, 255), width=2)
        d.text((px - 3, py - 7), str(num), font=font("DejaVuSans-Bold.ttf", 10),
               fill=(255, 255, 255))
    d.text((x0 + 10, y0 + h - 20), "Red dots = the 12 drawn stories above and below, numbered to match.",
           font=F_SMALL, fill=SOFT)


def card(d, x, y, w, h, num, kind, col, head, sub, hf, sf):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=2)
    d.rectangle([x, y, x + w, y + 5], fill=col)
    d.ellipse([x + 12, y + 14, x + 52, y + 54], fill=(232, 238, 245))
    icon(d, kind, x + 32, y + 34, 13, col)
    d.text((x + 62, y + 16), "STORY %d" % num, font=font("DejaVuSans-Bold.ttf", 13), fill=col)
    d.text((x + 62, y + 34), "19 NOV 2026", font=F_SMALL, fill=SOFT)
    yy = text_block(d, x + 12, y + 60, head, hf, w - 24)
    text_block(d, x + 12, yy + 3, sub, sf, w - 24)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead ----
    d.rectangle([0, 0, W, 8], fill=RED)
    d.text((24, 18), "THE WORLD IN ONE DAY  \u00b7  42 STORIES  \u00b7  7 REGIONS",
           font=F_KICK, fill=RED)
    d.text((24, 38), "Thursday 19 November 2026", font=F_TITLE, fill=INK)
    d.text((24, 98), "Trump, Xi & Putin meet in Shenzhen  \u00b7  World court rules on the Rohingya  \u00b7  Record $81.3bn Anthropic IPO  \u00b7  GTA VI launches",
           font=F_SUB, fill=SOFT)
    d.line([24, 122, W - 24, 122], fill=LINE, width=2)
    # ---- hero row: 4 big drawn stories ----
    cw, gap = 244, 8
    for i, (num, kind, col, head, sub, mx, my) in enumerate(HERO):
        card(d, 24 + i * (cw + gap), 132, cw, 158, num, kind, col, head, sub,
             F_HERO_H, F_HERO_S)
    # ---- map + side boxes ----
    draw_map(d, 24, 300, 632, 168)
    bx = 664
    d.rectangle([bx, 300, W - 24, 392], fill=(255, 248, 220), outline=RED, width=2)
    d.text((bx + 12, 308), "DATE CHECK \u2014 READ THIS FIRST", font=F_SMALL_B, fill=RED)
    yy = text_block(d, bx + 12, 328, "Every story here happened or was first reported Thu 19 Nov 2026.",
               F_SMALL_B, W - 24 - bx - 24)
    text_block(d, bx + 12, yy + 4, "Left out (wrong date): Maduro capture, 3 Jan 2026; 2017 Rohingya crackdown.",
               F_SMALL, W - 24 - bx - 24)
    d.rectangle([bx, 400, W - 24, 468], fill=CARD, outline=LINE, width=2)
    d.text((bx + 12, 408), "BY THE NUMBERS", font=F_SMALL_B, fill=INK)
    text_block(d, bx + 12, 428, "Hang Seng \u22121.9%  \u00b7  FTSE \u22121.3%  \u00b7  S&P 500 \u22120.2%  \u00b7  Brent $89.59  \u00b7  Gold $3,739.60  \u00b7  Bitcoin $63,552",
               F_SMALL, W - 24 - bx - 24)
    # ---- drawn stories 5-12, two rows of four ----
    for row, group in enumerate((DRAWN[:4], DRAWN[4:])):
        for i, (num, kind, col, head, sub, mx, my) in enumerate(group):
            card(d, 24 + i * (cw + gap), 478 + row * 168, cw, 158, num, kind, col,
                 head, sub, F_CARD_H, F_CARD_S)
    # ---- numbered briefs 13-42 ----
    y0 = 824
    d.line([24, y0 - 8, W - 24, y0 - 8], fill=LINE, width=2)
    d.text((24, y0), "THE REST OF THE DAY \u2014 30 MORE STORIES, 13\u201342",
           font=F_SEC, fill=INK)
    colw = 320
    for i, txt in enumerate(BRIEFS):
        col_i, row_i = i // 10, i % 10
        x = 24 + col_i * (colw + 8)
        y = y0 + 26 + row_i * 15
        d.text((x, y), "%d." % (13 + i), font=F_BRIEF_N, fill=RED)
        d.text((x + 26, y), txt, font=F_BRIEF, fill=INK)
    # ---- footer ----
    d.line([24, 1006, W - 24, 1006], fill=LINE, width=1)
    d.text((24, 1010), "All 42 stories happened or were first reported Thu 19 Nov 2026. Sources listed in SOURCES.md. make.fun news-image-20261119.",
           font=F_FOOT, fill=SOFT)
    img.save(OUT, "PNG", optimize=True)


if __name__ == "__main__":
    main()
