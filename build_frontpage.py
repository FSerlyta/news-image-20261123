#!/usr/bin/env python3
"""Build the news-image-20261123 front page (1024x1024 PNG) with Pillow.

Run locally only:  python3 build_frontpage.py  -> writes entry.png beside it.
The submitted program (main.py, stdlib only) just copies entry.png to
/output/entry.png, so the graded run needs no Pillow and no network.
All text comes from stories.json (50 stories, all reported 23 Nov 2026).
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (246, 241, 227)
INK = (20, 20, 20)
RED = (176, 30, 36)
BLUE = (31, 78, 121)
TEAL = (14, 107, 107)
GREY = (90, 86, 76)
LIGHT = (232, 226, 208)

FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/local/share/fonts",
)


def find_font_dir():
    for cand in FONT_DIRS:
        if os.path.isdir(cand):
            return cand
    return FONT_DIRS[0]


FD = find_font_dir()


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines, each fitting width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return lines


def center(draw, y, text, fnt, fill, cx=W // 2):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


# ---------------------------------------------------------------- art
def art_cop31(d, x, y, s):
    # Sun behind a dark cloud, thermometer at its side.
    cx, cy, r = x + s * 0.42, y + s * 0.42, s * 0.30
    for a in range(0, 360, 30):
        rad = math.radians(a)
        d.line([cx + math.cos(rad) * (r + 4), cy + math.sin(rad) * (r + 4),
                cx + math.cos(rad) * (r + 14), cy + math.sin(rad) * (r + 14)],
               fill=(214, 130, 30), width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 150, 40))
    d.ellipse([x + s * 0.55, y + s * 0.55, x + s * 0.98, y + s * 0.82],
              fill=(70, 70, 78))
    d.ellipse([x + s * 0.62, y + s * 0.44, x + s * 0.95, y + s * 0.72],
              fill=(70, 70, 78))
    d.rectangle([x + s * 0.60, y + s * 0.55, x + s * 0.97, y + s * 0.72],
                fill=(70, 70, 78))
    # thermometer
    tx = x + s * 0.08
    d.rectangle([tx, y + s * 0.55, tx + 10, y + s * 0.88], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([tx + 2, y + s * 0.62, tx + 8, y + s * 0.86], fill=RED)
    d.ellipse([tx - 3, y + s * 0.84, tx + 13, y + s * 1.0], fill=RED,
              outline=INK, width=2)


def art_hormuz(d, x, y, s):
    # Oil tanker on waves, smoke plume.
    d.rectangle([x + s * 0.06, y + s * 0.52, x + s * 0.94, y + s * 0.68],
                fill=(40, 48, 58))
    d.polygon([(x + s * 0.94, y + s * 0.52), (x + s * 0.99, y + s * 0.62),
               (x + s * 0.94, y + s * 0.68)], fill=(40, 48, 58))
    for i, c in enumerate([(176, 30, 36), (232, 150, 40), (31, 78, 121)]):
        d.rectangle([x + s * (0.12 + i * 0.20), y + s * 0.34,
                     x + s * (0.28 + i * 0.20), y + s * 0.52], fill=c,
                    outline=INK, width=1)
    d.rectangle([x + s * 0.74, y + s * 0.30, x + s * 0.86, y + s * 0.52],
                fill=(240, 240, 235), outline=INK, width=1)
    for cx, cy, r in [(0.80, 0.16, 9), (0.86, 0.10, 11), (0.90, 0.20, 8)]:
        d.ellipse([x + s * cx - r, y + s * cy - r, x + s * cx + r,
                   y + s * cy + r], fill=(120, 118, 112))
    for i in range(4):
        wx = x + s * (0.05 + i * 0.24)
        d.arc([wx, y + s * 0.72, wx + s * 0.22, y + s * 0.92], 0, 180,
              fill=BLUE, width=3)


def art_markets(d, x, y, s):
    # Falling red chart line with arrow.
    pts = [(x + s * 0.08, y + s * 0.22), (x + s * 0.28, y + s * 0.34),
           (x + s * 0.46, y + s * 0.30), (x + s * 0.64, y + s * 0.52),
           (x + s * 0.82, y + s * 0.78)]
    d.line(pts, fill=RED, width=5, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 2), (ex - 4, ey - 16)], fill=RED)
    for bx, bh in [(0.14, 0.30), (0.34, 0.22), (0.54, 0.16)]:
        d.rectangle([x + s * bx, y + s * (0.86 - bh), x + s * (bx + 0.10),
                     y + s * 0.86], fill=(200, 200, 192), outline=GREY, width=1)


def art_capitol(d, x, y, s):
    # US Capitol dome, simplified.
    d.rectangle([x + s * 0.10, y + s * 0.72, x + s * 0.90, y + s * 0.86],
                fill=(240, 240, 235), outline=INK, width=2)
    for i in range(5):
        cx = x + s * (0.20 + i * 0.15)
        d.rectangle([cx - 4, y + s * 0.56, cx + 4, y + s * 0.72],
                    fill=(240, 240, 235), outline=INK, width=1)
    d.pieslice([x + s * 0.28, y + s * 0.18, x + s * 0.72, y + s * 0.62],
               180, 360, fill=(240, 240, 235), outline=INK, width=2)
    d.rectangle([x + s * 0.46, y + s * 0.10, x + s * 0.54, y + s * 0.22],
                fill=(240, 240, 235), outline=INK, width=1)
    d.line([x + s * 0.50, y + s * 0.02, x + s * 0.50, y + s * 0.10],
           fill=INK, width=2)
    d.polygon([(x + s * 0.50, y + s * 0.02), (x + s * 0.66, y + s * 0.05),
               (x + s * 0.50, y + s * 0.08)], fill=RED)


def art_mercury(d, x, y, s):
    # Cratered Mercury + small spacecraft.
    cx, cy, r = x + s * 0.38, y + s * 0.55, s * 0.32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 160, 148),
              outline=INK, width=2)
    for dx, dy, cr in [(-0.12, -0.10, 7), (0.12, 0.08, 9), (-0.02, 0.16, 5),
                       (0.16, -0.14, 5)]:
        d.ellipse([cx + s * dx - cr, cy + s * dy - cr, cx + s * dx + cr,
                   cy + s * dy + cr], fill=(140, 132, 120))
    d.rectangle([x + s * 0.72, y + s * 0.16, x + s * 0.84, y + s * 0.28],
                fill=(31, 78, 121), outline=INK, width=1)
    d.rectangle([x + s * 0.60, y + s * 0.20, x + s * 0.72, y + s * 0.24],
                fill=BLUE, outline=INK, width=1)
    d.rectangle([x + s * 0.84, y + s * 0.20, x + s * 0.96, y + s * 0.24],
                fill=BLUE, outline=INK, width=1)
    d.line([x + s * 0.78, y + s * 0.28, cx + r * 0.7, cy - r * 0.7],
           fill=GREY, width=1)


ART = {"cop31": art_cop31, "hormuz": art_hormuz, "markets": art_markets,
       "capitol": art_capitol, "mercury": art_mercury}


# ---------------------------------------------------------------- page
def build():
    with open(os.path.join(HERE, "stories.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["leads"]) + len(data["second_leads"]) + len(data["briefs"]) + 1 == 50, \
        "story count must be 50"

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 20                      # side margin
    CW = W - 2 * MX              # content width

    # ---- masthead
    y = 12
    center(d, y, data["title"], SERIF_B(54), INK)
    y += 66
    d.line([MX, y, W - MX, y], fill=INK, width=3)
    y += 6
    dl = data["date"]
    f_dl = SANS_B(16)
    d.text((MX, y), dl, font=f_dl, fill=INK)
    right = "50 STORIES  ·  ONE DAY"
    w = d.textlength(right, font=SANS_B(14))
    d.text((W - MX - w, y + 1), right, font=SANS_B(14), fill=RED)
    y += 24
    d.line([MX, y, W - MX, y], fill=INK, width=2)
    y += 6
    tl = wrap(d, data["timeline"], SANS(11), CW)
    assert len(tl) == 1, "timeline must fit one line: %r" % tl
    d.text((MX, y), tl[0], font=SANS(11), fill=GREY)
    y += 18
    d.line([MX, y, W - MX, y], fill=INK, width=1)

    # ---- lead row A: two big stories
    y += 8
    rowA_h = 150
    x0, x1 = MX, MX + 592
    d.line([x1 - 8, y, x1 - 8, y + rowA_h], fill=GREY, width=1)
    for (lead, x, wdt) in [(data["leads"][0], x0, 572),
                            (data["leads"][1], x1, 392)]:
        art_w = 110
        tx = x
        tw = wdt - art_w - 12
        d.text((tx, y), lead["section"], font=SANS_B(12), fill=RED)
        hl = wrap(d, lead["headline"], SERIF_B(26), tw)
        assert len(hl) <= 2, "lead headline too long: %r" % lead["headline"]
        yy = y + 18
        for ln in hl:
            d.text((tx, yy), ln, font=SERIF_B(26), fill=INK)
            yy += 31
        dk = wrap(d, lead["deck"], SANS(13), tw)
        assert len(dk) <= 3, "lead deck too long: %r" % lead["deck"]
        for ln in dk:
            d.text((tx, yy), ln, font=SANS(13), fill=(40, 40, 40))
            yy += 17
        ART[lead["art"]](d, x + wdt - art_w, y + 28, art_w)
    y += rowA_h
    d.line([MX, y + 6, W - MX, y + 6], fill=INK, width=2)

    # ---- lead row B: three stories
    y += 12
    rowB_h = 104
    col_w = (CW - 2 * 16) // 3
    for i, lead in enumerate(data["second_leads"]):
        x = MX + i * (col_w + 16)
        if i:
            d.line([x - 8, y, x - 8, y + rowB_h], fill=GREY, width=1)
        art_w = 62
        tx = x
        tw = col_w - art_w - 8
        d.text((tx, y), lead["section"], font=SANS_B(11), fill=RED)
        hl = wrap(d, lead["headline"], SERIF_B(19), tw)
        assert len(hl) <= 2, "2nd-lead headline too long: %r" % lead["headline"]
        yy = y + 16
        for ln in hl:
            d.text((tx, yy), ln, font=SERIF_B(19), fill=INK)
            yy += 23
        dk = wrap(d, lead["deck"], SANS(11), tw)
        assert len(dk) <= 3, "2nd-lead deck too long: %r" % lead["deck"]
        for ln in dk:
            d.text((tx, yy), ln, font=SANS(11), fill=(40, 40, 40))
            yy += 14
        ART[lead["art"]](d, x + col_w - art_w, y + 30, art_w)
    y += rowB_h
    d.line([MX, y + 6, W - MX, y + 6], fill=INK, width=2)

    # ---- numbers strip
    y += 12
    num_h = 46
    box_w = (CW - 5 * 8) // 6
    for i, (num, label) in enumerate(data["numbers"]):
        x = MX + i * (box_w + 8)
        d.rectangle([x, y, x + box_w, y + num_h], outline=GREY, width=1,
                    fill=LIGHT)
        center(d, y + 2, num, SERIF_B(18), RED, cx=x + box_w // 2)
        ll = wrap(d, label, SANS(9), box_w - 10)
        assert len(ll) <= 2, "number label too long: %r" % label
        yy = y + 23
        for ln in ll:
            center(d, yy, ln, SANS(9), INK, cx=x + box_w // 2)
            yy += 10
    y += num_h + 8
    d.line([MX, y, W - MX, y], fill=INK, width=2)

    # ---- briefs header
    y += 6
    d.text((MX, y), "THE DAY IN BRIEF", font=SANS_B(14), fill=INK)
    rh = "44 MORE STORIES  ·  REPORTED 23 NOV 2026"
    w = d.textlength(rh, font=SANS_B(11))
    d.text((W - MX - w, y + 2), rh, font=SANS_B(11), fill=RED)
    y += 22

    # ---- briefs grid: 4 cols x 11 rows
    cols, rows = 4, 11
    gap = 14
    cell_w = (CW - (cols - 1) * gap) // cols
    cell_h = 41
    assert len(data["briefs"]) == cols * rows
    idx = 0
    for r in range(rows):
        for c in range(cols):
            b = data["briefs"][idx]
            idx += 1
            x = MX + c * (cell_w + gap)
            yy = y + r * cell_h
            # headline with red section tag on the first line
            tag = b["section"] + " — "
            full = tag + b["headline"]
            lines = wrap(d, full, SANS_B(11), cell_w)
            assert len(lines) <= 2, "brief headline too long: %r" % b["headline"]
            ly = yy
            for li, ln in enumerate(lines):
                if li == 0 and ln.startswith(tag):
                    d.text((x, ly), tag, font=SANS_B(11), fill=RED)
                    tw = d.textlength(tag, font=SANS_B(11))
                    d.text((x + tw, ly), ln[len(tag):], font=SANS_B(11),
                           fill=INK)
                else:
                    d.text((x, ly), ln, font=SANS_B(11), fill=INK)
                ly += 13
            deck = wrap(d, b["deck"], SANS(10), cell_w)
            assert len(deck) <= 1, "brief deck too long: %r" % b["deck"]
            d.text((x, ly), deck[0], font=SANS(10), fill=(60, 58, 50))
        # row rule
        if r < rows - 1:
            d.line([MX, y + (r + 1) * cell_h - 3, W - MX,
                    y + (r + 1) * cell_h - 3], fill=(214, 208, 190), width=1)
    y += rows * cell_h + 2

    # ---- late strip: the 50th story
    late = data["late"]
    d.line([MX, y, W - MX, y], fill=INK, width=2)
    y += 6
    tag = "LATE — "
    tw = d.textlength(tag, font=SANS_B(11))
    d.text((MX, y), tag, font=SANS_B(11), fill=RED)
    late_text = late["headline"] + " — " + late["deck"]
    ll = wrap(d, late_text, SANS(11), CW - tw)
    assert len(ll) == 1, "late line too long: %r" % ll
    d.text((MX + tw, y), ll[0], font=SANS(11), fill=INK)
    y += 18

    # ---- footer
    d.line([MX, y, W - MX, y], fill=INK, width=2)
    y += 8
    fl = wrap(d, data["footer"], SANS(10), CW)
    assert len(fl) <= 2, "footer too long"
    for ln in fl:
        center(d, y, ln, SANS(10), GREY)
        y += 13

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
