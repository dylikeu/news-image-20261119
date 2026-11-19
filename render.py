#!/usr/bin/env python3
"""Render the 19 November 2026 front page as a 1024x1024 PNG.

Draws a one-page newspaper: masthead with the day's date, the lead story
(Trump, Xi and Putin's first three-way summit in Shenzhen), a world map
with the day's locations, a DATE CHECK box, and 41 more stories in three
columns across six continents. All headlines come from the STORIES table
below, each checked against the day's live sources in SOURCES.md.

Deterministic: same input, same bytes, every run. Stdlib plus Pillow.
Run:  python3 render.py   (writes news.png next to this file)
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 227)
NAVY = (20, 38, 74)
NAVY_DARK = (13, 26, 52)
GOLD = (216, 164, 65)
RED = (178, 34, 34)
INK = (26, 26, 26)
GREY = (84, 84, 84)
SEA = (214, 229, 241)
LAND = (198, 211, 181)
LAND_EDGE = (150, 168, 138)
DOT = (192, 57, 43)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# (section, headline, deck) — 41 briefs; the lead story sits above them.
STORIES = [
    ("MIDDLE EAST",
     [("Iran strikes Gulf states after U.S. hit",
       "Drones hit Patriot sites in Kuwait, Bahrain"),
      ("Kuwait says it repelled Iranian attack",
       "Air defences engaged; no casualties reported"),
      ("Tanker struck near Khasab, Hormuz",
       "Engine room hit; crew safe, UKMTO says"),
      ("Houthi missile aimed at Riyadh shot down",
       "Coalition intercepts cruise missile"),
      ("Israel pushes ground operation in Gaza",
       "Troops move beyond the Yellow Line"),
      ("Eisenkot tapped to form Israel government",
       "Herzog bypasses Netanyahu")]),
    ("EUROPE",
     [("Ukraine hits Crimean Bridge a 3rd time",
       "Traffic halted after this week's strikes"),
      ("World court set to rule on Myanmar case",
       "Rohingya genocide ruling due"),
      ("Imamoglu sentenced in CHP case",
       "Ex-Istanbul mayor, eight others convicted"),
      ("France: 4th weekend of price protests",
       "Cost-of-living marches continue"),
      ("Five EU nations plan Rwanda asylum transfers",
       "Kigali scheme revived by five capitals")]),
    ("ASIA-PACIFIC",
     [("IAEA: N. Korea expanded uranium enrichment",
       "Yongbyon site grew, agency says"),
      ("Cyclone Aqwan nears India's east coast",
       "Bay of Bengal landfall expected"),
      ("S. Korea exam held under AI-cheating curbs",
       "Phones jammed at Seoul test centres"),
      ("Unrest in Bangladesh over Hasina's return",
       "Wage protests spread in Dhaka"),
      ("U.S., Philippines pursue $2bn+ loan package",
       "White House announces financing push"),
      ("Suicide bombing kills 5 in Pakistan",
       "Checkpoint attack injures 13")]),
    ("AMERICAS",
     [("Trump: Iran seeking chemical, biological arms",
       "President's claim raises stakes"),
      ("Iran agent jailed 27 years over Trump plot",
       "U.S. court sentences assassination plotter"),
      ("Judge extends block on Trump memorial arch",
       "Washington arch halted 14 more days"),
      ("Florida floods shut roads and schools",
       "Torrential rain swamps the state"),
      ("U.S., Venezuela restore military cooperation",
       "Military cooperation resumes")]),
    ("AFRICA",
     [("Ethiopia, Eritrea mass troops on border",
       "Forces build up amid war fears"),
      ("Sudan: drones drive civilian toll",
       "Aid reaches displaced at El Dabba"),
      ("Somalia crisis deepens over reforms",
       "Federal tensions rise in Mogadishu")]),
    ("OCEANIA",
     [("Fiji, Tonga declare drought emergencies",
       "El Nino blamed for water shortages"),
      ("Australia jobless rate rises to 4.9%",
       "Canberra reports softening labour market")]),
    ("MARKETS & TECH",
     [("Anthropic prices record IPO at $83 a share",
       "Biggest AI listing yet, debut today"),
      ("AI worries drag stocks lower",
       "Hang Seng -2.78%, FTSE 100 -1.30%"),
      ("Gold, copper and bitcoin slide",
       "Metals and crypto fall together"),
      ("GTA VI goes on sale after 13-year wait",
       "Consoles capped at 30 FPS on launch"),
      ("Waymo pulls driverless taxis off freeways",
       "U.S. robotaxi retreat in San Francisco"),
      ("IMF deal unlocks $2.3bn for Egypt",
       "Cairo programme resumes")]),
    ("SCIENCE & HEALTH",
     [("Strain-specific Ebola vaccines to be trialled",
       "DR Congo to test new shots"),
      ("Alzheimer's, brain-tumour studies advance",
       "UK research points to new treatments"),
      ("Webb confirms rare star merger",
       "Telescope confirms the merger"),
      ("Antarctic blue whales up tenfold",
       "Recovery since whaling ended")]),
    ("SPORT & CULTURE",
     [("Alcaraz beats Medvedev at ATP Finals",
       "Turin semi-final goes to the Spaniard"),
      ("Chelsea beat PSG 1-0 in women's UCL",
       "London win in Champions League"),
      ("England win ODI series in Australia",
       "Hobart decider seals the series"),
      ("'Human' is Cambridge word of the year",
       "Dictionary picks the word of 2026")]),
]

# Three columns: which sections go where (balanced by item count).
COLUMNS = [
    ["MIDDLE EAST", "EUROPE", "AFRICA"],
    ["ASIA-PACIFIC", "AMERICAS", "OCEANIA"],
    ["MARKETS & TECH", "SCIENCE & HEALTH", "SPORT & CULTURE"],
]

# Rough continent outlines, (lon, lat) — stylised, equirectangular.
CONTINENTS = [
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 72), (-100, 73),
     (-90, 74), (-82, 72), (-75, 70), (-68, 58), (-60, 52), (-55, 47),
     (-60, 43), (-70, 42), (-75, 35), (-80, 31), (-81, 26), (-84, 30),
     (-89, 21), (-92, 16), (-97, 16), (-105, 20), (-112, 25), (-118, 32),
     (-124, 40), (-124, 48), (-132, 58), (-145, 60), (-155, 58),
     (-162, 58), (-168, 62)],
    [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-44, -2), (-35, -8),
     (-38, -15), (-42, -22), (-48, -27), (-55, -33), (-62, -38),
     (-68, -45), (-70, -52), (-73, -45), (-73, -35), (-72, -22),
     (-78, -10), (-81, -3), (-80, 3)],
    [(-17, 15), (-15, 22), (-10, 29), (-5, 35), (0, 36), (9, 37),
     (15, 32), (20, 32), (30, 31), (33, 28), (36, 22), (40, 15),
     (44, 11), (51, 11), (48, 2), (42, -5), (40, -12), (36, -18),
     (33, -25), (30, -32), (25, -34), (18, -35), (15, -30), (13, -20),
     (12, -12), (12, -5), (9, 3), (0, 5), (-8, 5), (-13, 8), (-16, 12)],
    [(-9, 37), (-9, 43), (-2, 47), (-1, 49), (2, 51), (5, 53), (8, 55),
     (8, 57), (10, 59), (14, 58), (18, 56), (21, 55), (24, 58), (26, 59),
     (28, 61), (25, 64), (22, 68), (18, 70), (14, 67), (12, 62), (8, 58),
     (5, 58), (2, 54), (-2, 50), (-5, 47), (-9, 42)],
    [(30, 62), (35, 66), (42, 68), (52, 69), (62, 70), (72, 72),
     (85, 74), (100, 77), (115, 73), (130, 72), (145, 72), (160, 69),
     (178, 65), (172, 62), (162, 58), (158, 52), (150, 59), (142, 52),
     (140, 45), (135, 43), (130, 40), (127, 38), (122, 32), (118, 28),
     (110, 21), (108, 18), (105, 10), (100, 8), (97, 10), (94, 17),
     (90, 20), (86, 20), (80, 13), (77, 8), (74, 15), (70, 22),
     (66, 25), (61, 25), (57, 26), (54, 27), (50, 29), (47, 30),
     (44, 29), (40, 31), (36, 33), (33, 36), (30, 36)],
    [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
     (130, -32), (135, -35), (138, -35), (140, -38), (145, -38),
     (150, -37), (153, -32), (152, -27), (150, -23), (146, -19),
     (142, -11), (137, -12), (132, -12), (127, -14), (122, -17),
     (118, -20)],
]

# (lon, lat, label or None, label dx, label dy)
DOTS = [
    (114.1, 22.5, "SHENZHEN", 8, -4),
    (48.0, 29.0, "GULF", -6, -16),
    (34.5, 31.5, "GAZA", -42, -4),
    (34.0, 45.0, "CRIMEA", -10, -16),
    (46.7, 24.6, "RIYADH", 8, 4),
    (56.2, 26.2, None, 0, 0),
    (127.0, 37.5, "SEOUL", 8, -4),
    (90.4, 23.8, None, 0, 0),
    (86.0, 20.0, None, 0, 0),
    (73.0, 33.7, None, 0, 0),
    (-0.1, 51.5, None, 0, 0),
    (2.35, 48.85, None, 0, 0),
    (32.85, 39.9, None, 0, 0),
    (7.7, 45.07, None, 0, 0),
    (-77.0, 38.9, None, 0, 0),
    (-81.0, 28.0, None, 0, 0),
    (-122.4, 37.8, None, 0, 0),
    (-66.9, 10.5, None, 0, 0),
    (38.7, 9.0, None, 0, 0),
    (32.5, 15.6, None, 0, 0),
    (45.3, 2.0, None, 0, 0),
    (15.3, -4.3, None, 0, 0),
    (149.1, -35.3, None, 0, 0),
    (178.4, -17.7, None, 0, 0),
    (184.8, -21.1, None, 0, 0),
]

DATE_CHECK_BODY = (
    "Every story on this page happened or was first reported on "
    "Thursday 19 November 2026.",
    "Left out on purpose \u2014 18 Nov news: EU\u2013Indonesia trade pact; "
    "U.S. measles-elimination loss; Alaska Senate result; EU \u20ac45bn "
    "Ukraine loan; Voyager 1 one light-day.",
)

FOOTER = ("S&P 500 7,324 (-0.23%)  \u00b7  HANG SENG -2.78%  \u00b7  "
          "FTSE 100 10,551 (-1.30%)  \u00b7  BRENT $89.30")


def wrap(text, fnt, max_w, max_lines=3):
    """Greedy word wrap to at most max_lines lines; ellipsis if longer."""
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and words and not lines[-1].endswith("\u2026"):
        # Something was left over: mark the last line as truncated.
        joined = " ".join(lines)
        if len(joined) < len(text):
            while lines and fnt.getlength(lines[-1] + "\u2026") > max_w:
                lines[-1] = lines[-1].rsplit(" ", 1)[0]
            lines[-1] += "\u2026"
    return lines


def text_halo(draw, xy, s, fnt, fill, halo=(255, 255, 255)):
    x, y = xy
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((x + dx, y + dy), s, font=fnt, fill=halo)
    draw.text((x, y), s, font=fnt, fill=fill)


def column_height(sections, head_f, sub_f, gap, col_w):
    """Total height of a column's sections at the given fonts."""
    total = 0
    for header, items in sections:
        total += 20  # header + rule
        for headline, sub in items:
            lines = wrap(headline, head_f, col_w, max_lines=2)
            total += len(lines) * 15 + 13 + gap
    return total


def draw_columns(draw, top, bottom, col_w):
    """Lay out the three story columns; shrink fonts until they fit."""
    by_name = dict(STORIES)
    x_starts = [16, 354, 692]
    for head_size, sub_size, gap in ((13, 11, 7), (12, 10, 6), (11, 10, 5)):
        head_f = font(SANS_B, head_size)
        sub_f = font(SANS, sub_size)
        sect_f = font(SANS_B, 14)
        heights = []
        for names in COLUMNS:
            sections = [(n, by_name[n]) for n in names]
            heights.append(column_height(sections, head_f, sub_f, gap, col_w))
        if max(heights) <= bottom - top:
            break
    for x0, names in zip(x_starts, COLUMNS):
        y = top
        for name in names:
            items = by_name[name]
            draw.text((x0, y), name, font=sect_f, fill=RED)
            y += 18
            draw.line([(x0, y), (x0 + col_w, y)], fill=RED, width=1)
            y += 6
            for headline, sub in items:
                for line in wrap(headline, head_f, col_w, max_lines=2):
                    draw.text((x0, y), line, font=head_f, fill=NAVY)
                    y += 15
                for line in wrap(sub, sub_f, col_w, max_lines=1):
                    draw.text((x0, y), line, font=sub_f, fill=GREY)
                    y += 13
                y += gap
            y += 6
    return head_size


def draw_map(draw, box):
    """Stylised world map with red dots on the day's locations."""
    x0, y0, w, h = box
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA,
                   outline=LAND_EDGE, width=1)

    def proj(lon, lat):
        return (x0 + (lon + 170.0) / 360.0 * w,
                y0 + (84.0 - lat) / 142.0 * h)

    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    label_f = font(SANS_B, 10)
    for lon, lat, label, dx, dy in DOTS:
        px, py = proj(lon, lat)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=DOT,
                     outline=(255, 255, 255), width=1)
        if label:
            text_halo(draw, (px + dx, py + dy), label, label_f, NAVY)
    # Title last, with a halo, so the land never covers it.
    text_halo(draw, (x0 + 8, y0 + 5), "WHERE TODAY HAPPENED",
              font(SANS_B, 11), NAVY, halo=SEA)


def draw_date_check(draw, box):
    x0, y0, w, h = box
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 255, 255),
                   outline=RED, width=3)
    title_f = font(SANS_B, 20)
    body_f = font(SANS, 12)
    draw.text((x0 + 12, y0 + 10), "DATE CHECK", font=title_f, fill=RED)
    y = y0 + 40
    for para in DATE_CHECK_BODY:
        for line in wrap(para, body_f, w - 24, max_lines=4):
            draw.text((x0 + 12, y), line, font=body_f, fill=INK)
            y += 16
        y += 4


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead.
    draw.rectangle([0, 0, W, 96], fill=NAVY)
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 62)
    draw.text(((W - tf.getlength(title)) / 2, 6), title, font=tf,
              fill=(255, 255, 255))
    date = "THURSDAY, 19 NOVEMBER 2026"
    df = font(SANS_B, 25)
    draw.text(((W - df.getlength(date)) / 2, 66), date, font=df, fill=GOLD)

    # Lead kicker.
    kf = font(SANS_B, 15)
    draw.text((16, 106), "LEAD STORY  \u00b7  SHENZHEN \u2014 FIRST THREE-WAY SUMMIT",
              font=kf, fill=RED)
    right = "42 STORIES  \u00b7  6 CONTINENTS"
    draw.text((W - 16 - kf.getlength(right), 106), right, font=kf, fill=RED)

    # Lead headline + deck.
    hf = font(SERIF_B, 46)
    draw.text((16, 128), "TRUMP, XI & PUTIN MEET", font=hf, fill=NAVY)
    draw.text((16, 176), "IN SHENZHEN", font=hf, fill=NAVY)
    deck = ("The U.S., Chinese and Russian leaders hold their first "
            "three-way summit, on the APEC sidelines. Agenda: Ukraine, "
            "Iran, nuclear arms, trade and AI.")
    deck_f = font(SANS, 16)
    y = 228
    for line in wrap(deck, deck_f, W - 32, max_lines=2):
        draw.text((16, y), line, font=deck_f, fill=(68, 68, 68))
        y += 20

    # Map + date check row.
    draw_map(draw, (16, 274, 590, 134))
    draw_date_check(draw, (622, 274, 386, 134))

    # Story columns.
    draw_columns(draw, 422, 984, 316)

    # Markets footer.
    draw.rectangle([0, 992, W, H], fill=NAVY)
    ff = font(SANS_B, 15)
    draw.text(((W - ff.getlength(FOOTER)) / 2, 1002), FOOTER, font=ff,
              fill=(255, 255, 255))
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "news.png")
    render().save(out, "PNG", optimize=True)
    data = open(out, "rb").read()
    print("news.png:", len(data), "bytes")
    print("sha256:", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
