#!/usr/bin/env python3
"""Render the news-summary infographic for make.fun news-image-20261119.

One page, 1024x1024 PNG: the world's news of Thursday 19 November 2026.
42 stories, 6 continents, masthead date, world map, DATE CHECK box.
Stories verified against live reporting on 19 Nov 2026 (OneTurn, Roman
Report / Middle East Forum, Dubai Standard, The Paris Eye, News Media
House, AppiSToS, Times of India). See SOURCES.md.
Deterministic output: same bytes every run (no timestamps, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = (250, 246, 238)
NAVY = (15, 36, 64)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
INK = (20, 33, 61)
MUTED = (91, 100, 114)
TILE = (255, 255, 255)
BORDER = (227, 220, 203)
MAPLAND = (198, 210, 196)
MAPSEA = (222, 232, 240)

F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# (section, headline, detail) — 41 briefs + 1 lead = 42 stories
SECTIONS = [
    ("MIDDLE EAST", [
        ("Iran strikes Gulf states after U.S. hit",
         "Drones hit Kuwait's Ali Al Salem base and Bahrain"),
        ("Kuwait says it repelled Iranian attack",
         "Air defences engaged; no casualties reported"),
        ("Tanker struck near Khasab in Hormuz",
         "Engine room hit; crew safe, UKMTO says"),
        ("Houthi missile aimed at Riyadh shot down",
         "Saudis plan long Yemen campaign"),
        ("Israel pushes ground operation in Gaza",
         "Troops move beyond the Yellow Line"),
        ("Eisenkot tapped to form Israel government",
         "President bypasses Netanyahu"),
    ]),
    ("EUROPE", [
        ("Ukraine hits Crimean Bridge a 3rd time",
         "Traffic closed; damage being assessed"),
        ("World court set to rule on Myanmar case",
         "ICJ genocide ruling on the Rohingya"),
        ("Imamoglu sentenced in CHP case",
         "Ex-Istanbul mayor + 8 others, Ankara court"),
        ("France: 4th weekend of price protests",
         "Nationwide marches against prices"),
        ("Five EU states plan Rwanda asylum transfers",
         "Kigali scheme revived by five capitals"),
    ]),
    ("ASIA-PACIFIC", [
        ("IAEA: N. Korea expanded uranium enrichment",
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
         "Checkpoint attack injures 13"),
    ]),
    ("AMERICAS", [
        ("Trump: Iran seeks chemical, biological arms",
         "President's claim raises stakes"),
        ("Iran agent jailed 27 years over Trump plot",
         "U.S. court sentences assassination plotter"),
        ("Judge extends block on Trump memorial arch",
         "Washington arch halted 14 more days"),
        ("Florida floods shut roads and schools",
         "Torrential rain swamps the state"),
        ("U.S., Venezuela restore military cooperation",
         "First contact since Maduro's capture"),
    ]),
    ("AFRICA", [
        ("Ethiopia, Eritrea mass troops on border",
         "Forces build up amid war fears"),
        ("Sudan: drones drive civilian toll",
         "Aid reaches displaced at El Dabba"),
        ("Somalia crisis deepens over reforms",
         "Federal tensions rise in Mogadishu"),
    ]),
    ("OCEANIA", [
        ("Fiji, Tonga declare drought emergencies",
         "Water shortages across the Pacific"),
        ("Australia jobless rate rises to 4.9%",
         "Canberra reports softening labour market"),
    ]),
    ("MARKETS & TECH", [
        ("Anthropic prices record IPO at $83 a share",
         "Biggest AI listing yet; debut today"),
        ("AI worries drag stocks lower",
         "Hang Seng -2.78%, FTSE 100 -1.30%"),
        ("Gold, copper and bitcoin slide",
         "War and AI fears hit haven assets"),
        ("GTA VI goes on sale after 13-year wait",
         "Consoles capped at 30 fps at launch"),
        ("Waymo pulls driverless taxis off freeways",
         "U.S. robotaxi retreat in San Francisco"),
        ("IMF deal unlocks $2.3bn for Egypt",
         "Cairo programme resumes"),
    ]),
    ("SCIENCE & HEALTH", [
        ("Strain-specific Ebola vaccines to be trialled",
         "DR Congo to test new shots"),
        ("Alzheimer's, brain-tumour studies advance",
         "UK research points to new treatments"),
        ("Webb confirms rare star merger",
         "Supergiant swallowed a sun-like star"),
        ("Antarctic blue whales up tenfold",
         "Recovery since whaling ended"),
    ]),
    ("SPORT & CULTURE", [
        ("Alcaraz beats Medvedev at ATP Finals",
         "Turin semi-final goes to the Spaniard"),
        ("Chelsea beat PSG 1-0 in women's UCL",
         "London win in Champions League"),
        ("England win ODI series in Australia",
         "Hobart decider seals the series"),
        ("'Human' is Cambridge word of the year",
         "Dictionary picks the word of 2026"),
    ]),
]

# Simplified world map (lon, lat) polygons, equirectangular
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 66),
     (-80, 73), (-75, 62), (-70, 44), (-75, 35), (-80, 26), (-85, 30),
     (-90, 21), (-97, 16), (-105, 20), (-115, 30), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60), (-168, 66)],
    [(-58, 64), (-45, 60), (-40, 70), (-55, 76), (-65, 76), (-58, 64)],
    [(-78, 7), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-40, -5),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -45), (-70, -52),
     (-73, -40), (-73, -20), (-77, -12), (-80, -5), (-78, 7)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 2), (40, -5), (40, -15), (35, -25), (28, -33),
     (18, -35), (12, -18), (9, 4), (-8, 5), (-17, 15)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (18, 56),
     (21, 55), (24, 59), (30, 60), (30, 70), (40, 68), (50, 69), (60, 70),
     (70, 72), (80, 73), (90, 75), (100, 77), (110, 74), (120, 73),
     (130, 72), (140, 72), (150, 70), (158, 69), (162, 60), (170, 66),
     (178, 65), (170, 60), (162, 58), (158, 52), (150, 60), (142, 55),
     (140, 45), (135, 42), (130, 38), (127, 35), (122, 32), (120, 28),
     (110, 20), (108, 12), (105, 9), (100, 8), (98, 15), (92, 16), (88, 22),
     (80, 13), (77, 8), (72, 20), (66, 25), (61, 25), (57, 26), (52, 26),
     (50, 29), (48, 30), (44, 29), (40, 31), (36, 36), (30, 36), (26, 38),
     (23, 36), (19, 40), (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37),
     (-10, 36)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-5, 50)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (153, -20), (146, -19),
     (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (118, -20),
     (113, -22)],
    [(95, 5), (100, 0), (104, -3), (110, -7), (114, -8), (119, -9),
     (120, -10), (122, -8), (128, -4), (131, -1), (136, -2), (141, -8),
     (138, -8), (131, -7), (125, -6), (120, -3), (115, -1), (110, 0),
     (105, 2), (100, 5), (95, 5)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
     (143, 43), (145, 44), (142, 42), (140, 39), (138, 37), (135, 35),
     (132, 33), (130, 31)],
]
# (lon, lat, label or None, label dx, label dy) — story locations on the map
DOTS = [
    (114, 22, "SHENZHEN", 6, -6), (56, 27, "GULF", 6, 4),
    (34, 45, "CRIMEA", -62, -14), (4, 52, None, 0, 0),
    (126, 39, None, 0, 0), (89, 15, None, 0, 0), (34, 31, "GAZA", 6, 6),
    (39, 9, None, 0, 0), (32, 15, None, 0, 0), (178, -18, None, 0, 0),
    (149, -35, None, 0, 0), (-77, 39, None, 0, 0), (0, 51, None, 0, 0),
    (7, 45, None, 0, 0), (33, 40, None, 0, 0), (47, 25, None, 0, 0),
    (48, 29, None, 0, 0),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.rectangle([0, 0, W, 104], fill=NAVY)
f_title = font(F_SERIF_B, 52)
d.text((W // 2, 10), "THE WORLD TODAY", font=f_title, fill=(255, 255, 255), anchor="ma")
f_date = font(F_SANS_B, 24)
d.text((W // 2, 66), "THURSDAY,  19  NOVEMBER  2026", font=f_date, fill=GOLD, anchor="ma")

# ---- lead story ----
f_kick = font(F_SANS_B, 17)
d.text((20, 116), "LEAD STORY  ·  SHENZHEN — FIRST THREE-WAY SUMMIT", font=f_kick, fill=RED, anchor="la")
f_count = font(F_SANS_B, 15)
d.text((W - 20, 116), "42 STORIES · 6 CONTINENTS", font=f_count, fill=RED, anchor="ra")
f_head = font(F_SERIF_B, 40)
d.text((20, 138), "TRUMP, XI & PUTIN MEET", font=f_head, fill=INK, anchor="la")
d.text((20, 182), "IN SHENZHEN", font=f_head, fill=INK, anchor="la")
f_sub = font(F_SANS, 18)
sub = ("The U.S., Chinese and Russian leaders hold their first three-way summit, "
       "on the APEC sidelines. Agenda: Ukraine, Iran, nuclear arms, trade and AI.")
for i, line in enumerate(wrap(d, sub, f_sub, W - 40)):
    d.text((20, 230 + i * 23), line, font=f_sub, fill=MUTED, anchor="la")
d.line([20, 288, W - 20, 288], fill=BORDER, width=2)

# ---- map panel ----
MX0, MY0, MX1, MY1 = 16, 296, 620, 428
d.rectangle([MX0, MY0, MX1, MY1], fill=MAPSEA, outline=BORDER, width=2)


def mxy(lon, lat):
    x = MX0 + 8 + (lon + 170) / 360.0 * (MX1 - MX0 - 16)
    y = MY0 + 6 + (80 - lat) / 140.0 * (MY1 - MY0 - 12)
    return x, y


for poly in CONTINENTS:
    d.polygon([mxy(lon, lat) for lon, lat in poly], fill=MAPLAND)
f_map = font(F_SANS_B, 11)
d.text((MX0 + 10, MY0 + 6), "WHERE TODAY HAPPENED", font=f_map, fill=NAVY, anchor="la")
f_dot = font(F_SANS_B, 10)
for lon, lat, label, dx, dy in DOTS:
    x, y = mxy(lon, lat)
    d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=RED, outline=(255, 255, 255), width=1)
    if label:
        d.text((x + dx, y + dy), label, font=f_dot, fill=INK, anchor="la")

# ---- DATE CHECK box ----
BX0, BY0, BX1, BY1 = 636, 296, 1008, 428
d.rectangle([BX0, BY0, BX1, BY1], fill=TILE, outline=RED, width=3)
f_dc_head = font(F_SANS_B, 17)
d.text((BX0 + 12, BY0 + 8), "DATE CHECK", font=f_dc_head, fill=RED, anchor="la")
f_dc = font(F_SANS, 13)
dc_text = ("Every story on this page happened or was first reported on "
           "Thursday 19 November 2026.")
for i, line in enumerate(wrap(d, dc_text, f_dc, BX1 - BX0 - 24)):
    d.text((BX0 + 12, BY0 + 34 + i * 17), line, font=f_dc, fill=INK, anchor="la")
f_dc2 = font(F_SANS, 12)
dc2 = ("Left out on purpose — 18 Nov news: EU-Indonesia trade pact; "
       "U.S. measles-elimination loss; Alaska Senate result; EU 45bn "
       "Ukraine loan; Voyager 1 one light-day.")
for i, line in enumerate(wrap(d, dc2, f_dc2, BX1 - BX0 - 24)):
    d.text((BX0 + 12, BY0 + 76 + i * 15), line, font=f_dc2, fill=MUTED, anchor="la")

# ---- briefs: 3 columns, sections in order ----
COL_X = [16, 352, 688]
COL_W = 320
TOP = 440
BOTTOM = 956


def split_columns(counts):
    flat = []
    for sec, items in SECTIONS:
        flat.append(("sec", sec))
        for head, det in items:
            flat.append(("item", (head, det, sec)))
    cols = [[], [], []]
    idx = 0
    for ci in range(3):
        take, n = counts[ci], 0
        if idx < len(flat) and flat[idx][0] == "item":
            cols[ci].append(("sec", flat[idx][1][2]))
        while idx < len(flat) and n < take:
            kind, payload = flat[idx]
            if kind == "sec":
                cols[ci].append(("sec", payload))
                idx += 1
            else:
                cols[ci].append(("item", payload))
                n += 1
                idx += 1
        # drop a trailing orphan header (its items start the next column)
        if cols[ci] and cols[ci][-1][0] == "sec":
            cols[ci].pop()
    return cols


def measure(cols, hs, ds):
    f_h = font(F_SANS_B, hs)
    f_dt = font(F_SANS, ds)
    heights = []
    for ci in range(3):
        y = 0
        for kind, payload in cols[ci]:
            if kind == "sec":
                y += 17
            else:
                head, det, _sec = payload
                hl = wrap(d, head, f_h, COL_W)
                dl = wrap(d, det, f_dt, COL_W)
                y += len(hl) * (hs + 3) + len(dl) * (ds + 3) + 5
        heights.append(y)
    return heights


cols = split_columns([14, 13, 14])
for hs, ds in [(12, 10), (11, 10), (11, 9)]:
    heights = measure(cols, hs, ds)
    if max(heights) <= BOTTOM - TOP:
        break
print("column heights:", heights, "head", hs, "detail", ds)

f_h = font(F_SANS_B, hs)
f_dt = font(F_SANS, ds)
f_sec = font(F_SANS_B, 12)
for ci in range(3):
    x = COL_X[ci]
    y = TOP
    for kind, payload in cols[ci]:
        if kind == "sec":
            d.text((x, y), payload, font=f_sec, fill=RED, anchor="la")
            d.line([x, y + 14, x + COL_W, y + 14], fill=BORDER, width=1)
            y += 17
        else:
            head, det, _sec = payload
            hl = wrap(d, head, f_h, COL_W)
            for i, line in enumerate(hl):
                d.text((x, y + i * (hs + 3)), line, font=f_h, fill=INK, anchor="la")
            y += len(hl) * (hs + 3)
            dl = wrap(d, det, f_dt, COL_W)
            for i, line in enumerate(dl):
                d.text((x, y + i * (ds + 3)), line, font=f_dt, fill=MUTED, anchor="la")
            y += len(dl) * (ds + 3) + 5

# ---- footer ----
d.rectangle([0, 962, W, H], fill=NAVY)
foot_text = ("S&P 500  -0.23%   ·   HANG SENG  -2.78%   ·   FTSE 100  -1.30%   ·   "
             "BRENT $89.30   ·   GOLD, COPPER & BITCOIN DOWN")
f_foot = font(F_SANS_B, 17)
while d.textlength(foot_text, font=f_foot) > W - 32 and f_foot.size > 12:
    f_foot = font(F_SANS_B, f_foot.size - 1)
d.text((W // 2, 980), foot_text, font=f_foot, fill=(255, 255, 255), anchor="ma")

img.save(os.path.join(HERE, "news.png"), "PNG", optimize=True)
print("saved news.png")
