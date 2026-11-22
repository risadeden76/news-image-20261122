#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

Original artwork drawn programmatically with Pillow in this session:
no photo, logo or published image is copied. Every shape and glyph is
vector-drawn from code; the text is the day's verified news (see README).

Run:  python3 draw.py   -> writes entry.png beside this file.
The PNG is fully deterministic: same code, same bytes.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28  # page margin

PAPER = (247, 242, 231)
INK = (20, 39, 60)
RED = (179, 39, 30)
NAVY = (18, 42, 68)
NAVY_LT = (38, 68, 99)
TEAL = (14, 107, 107)
GOLD = (176, 124, 22)
WHITE = (255, 253, 246)
MUTED = (216, 222, 230)
GREY = (90, 96, 104)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap using real glyph widths."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, lines, f, fill, leading):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_globe(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], outline=color, width=3)
    d.line([(cx - r, cy), (cx + r, cy)], fill=color, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 0, 360, fill=color, width=3)
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=RED, width=5)


def icon_trade(d, x, y, s, color):
    # stacked shipping containers + small rising arrow
    d.rectangle([x, y + s * 0.55, x + s * 0.5, y + s * 0.9], fill=color)
    d.rectangle([x + s * 0.55, y + s * 0.55, x + s * 0.95, y + s * 0.9],
                fill=color)
    d.rectangle([x + s * 0.25, y + s * 0.18, x + s * 0.75, y + s * 0.5],
                fill=GOLD)
    d.line([(x + s * 0.85, y + s * 0.12), (x + s * 0.85, y - s * 0.05)],
           fill=RED, width=4)
    d.polygon([(x + s * 0.85, y - s * 0.08), (x + s * 0.68, y + s * 0.12),
               (x + s, y + s * 0.12)], fill=RED)


def icon_flags(d, x, y, s):
    # two small meeting flags side by side: US stripes, China red field
    fw, fh = s * 0.44, s * 0.62
    for i in range(5):
        d.rectangle([x, y + i * fh / 5, x + fw, y + (i + 1) * fh / 5],
                    fill=RED if i % 2 == 0 else WHITE, outline=INK, width=1)
    d.rectangle([x, y, x + fw * 0.45, y + fh * 0.45], fill=NAVY)
    for dx, dy in [(0.11, 0.12), (0.28, 0.12), (0.11, 0.3), (0.28, 0.3)]:
        px, py = x + fw * dx, y + fh * dy
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=WHITE)
    cx0 = x + fw + 6
    d.rectangle([cx0, y, cx0 + fw, y + fh], fill=RED, outline=INK, width=1)
    for sx, sy in [(0.22, 0.25), (0.5, 0.35), (0.72, 0.28), (0.45, 0.6),
                   (0.68, 0.62)]:
        px, py = cx0 + fw * sx, y + fh * sy
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD)


def icon_shield(d, cx, cy, r, color):
    pts = [(cx, cy - r), (cx + r * 0.85, cy - r * 0.45), (cx + r * 0.85, cy + r * 0.1),
           (cx, cy + r), (cx - r * 0.85, cy + r * 0.1), (cx - r * 0.85, cy - r * 0.45)]
    d.polygon(pts, outline=color, width=4)
    d.ellipse([cx - 7, cy - 8, cx + 7, cy + 6], fill=RED)
    d.rectangle([cx - 4, cy + 2, cx + 4, cy + 16], fill=RED)


def draw_lead_art(d, x0, y0, x1, y1):
    """Radar dish, missile arcs and Gulf waves on the lead panel."""
    # radar dish
    px, py = x0 + 95, y1 - 105
    d.arc([px - 85, py - 85, px + 85, py + 85], 235, 305, fill=(120, 160, 200), width=6)
    d.arc([px - 55, py - 55, px + 55, py + 55], 235, 305, fill=(120, 160, 200), width=4)
    d.line([(px, py), (px + 62, py - 62)], fill=(150, 190, 220), width=4)
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=GOLD)
    # missile arcs
    for i, (bx, by, ex, ey) in enumerate([
            (x0 + 10, y0 + 150, x0 + 210, y0 + 30),
            (x0 + 40, y0 + 175, x0 + 260, y0 + 70),
            (x0 + 70, y0 + 195, x0 + 300, y0 + 110)]):
        steps = 24
        pts = []
        for t in range(steps + 1):
            tt = t / steps
            mx = bx + (ex - bx) * tt
            my = by + (ey - by) * tt - 55 * math.sin(math.pi * tt)
            pts.append((mx, my))
        d.line(pts, fill=(232, 196, 120) if i == 1 else (150, 190, 220), width=3)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=RED)
    # waves at the bottom
    for k, wy in enumerate([y1 - 52, y1 - 34, y1 - 16]):
        pts = []
        for xx in range(x0, x1 + 1, 8):
            pts.append((xx, wy + 5 * math.sin((xx - x0) / 34.0 + k)))
        d.line(pts, fill=(70, 110, 150), width=3)
    # small tanker silhouette
    sx, sy = x1 - 150, y1 - 78
    d.polygon([(sx, sy), (sx + 110, sy), (sx + 96, sy + 22), (sx + 14, sy + 22)],
              fill=(150, 190, 220))
    d.rectangle([sx + 30, sy - 18, sx + 52, sy], fill=(150, 190, 220))
    d.line([(sx + 41, sy - 30), (sx + 41, sy - 18)], fill=(150, 190, 220), width=3)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # double frame
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    d.rectangle([16, 16, W - 17, H - 17], outline=RED, width=1)

    # ---- masthead
    f_title = font(SERIF, 58)
    d.text((W // 2, 30), "THE WORLD IN ONE DAY", font=f_title, fill=INK,
           anchor="ma")
    f_date = font(SANS_B, 27)
    d.text((W // 2, 102), "SUNDAY  ·  22 NOVEMBER 2026", font=f_date,
           fill=RED, anchor="ma")
    d.rectangle([M, 146, W - M, 150], fill=INK)
    d.rectangle([M, 153, W - M, 158], fill=RED)

    # ---- lead story: the Gulf
    lx0, ly0, lx1, ly1 = M, 172, W - M, 486
    d.rounded_rectangle([lx0, ly0, lx1, ly1], radius=12, fill=NAVY)
    f_kick = font(SANS_B, 23)
    d.text((lx0 + 26, ly0 + 20), "THE GULF  —  LEAD STORY", font=f_kick,
           fill=(232, 196, 120))
    f_head = font(SERIF, 46)
    head = wrap(d, "IRAN STRIKES U.S. RADARS IN BAHRAIN", f_head, 600)
    draw_text_block(d, lx0 + 26, ly0 + 56, head, f_head, WHITE, 52)
    f_sub = font(SANS, 23)
    sub = wrap(d, "Tehran claims missile and drone hits on two Patriot "
               "radars; tankers struck off Oman as the Gulf crisis "
               "deepens.", f_sub, 600)
    draw_text_block(d, lx0 + 26, ly0 + 56 + 52 * len(head) + 12, sub, f_sub,
                    MUTED, 29)
    draw_lead_art(d, 660, ly0 + 10, lx1 - 14, ly1 - 14)

    # ---- 2 x 2 story grid
    panels = [
        ("CLIMATE  ·  COP31, TURKEY", TEAL,
         "COP31 STALLS ON FOSSIL FUELS",
         "Talks run into overtime in Turkey — no deal on fossil "
         "fuels yet.", "globe"),
        ("TRADE  ·  BRUSSELS – JAKARTA", GOLD,
         "EU–INDONESIA SEAL LANDMARK DEAL",
         "After a decade of talks, the pact scraps 98.5% of "
         "tariffs.", "trade"),
        ("SUMMIT  ·  CHINA", NAVY,
         "TRUMP TO ADDRESS U.S. AFTER XI TALKS",
         "To speak after the Xi summit; eyes a 20-year Iran "
         "deal.", "flags"),
        ("CYBER  ·  WASHINGTON", RED,
         "FBI PROBES HACK OF CRIME DATABASE",
         "The bureau probes an apparent breach of its criminal "
         "records.", "shield"),
    ]
    gx = [M, 522]
    gy = [502, 680]
    pw, ph = 474, 162
    f_pkick = font(SANS_B, 19)
    f_phead = font(SERIF, 27)
    f_pbody = font(SANS, 20)
    for i, (kick, color, head, body, icon) in enumerate(panels):
        x0 = gx[i % 2]
        y0 = gy[i // 2]
        d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=10,
                            fill=WHITE, outline=INK, width=2)
        d.rounded_rectangle([x0, y0, x0 + pw, y0 + 9], radius=4, fill=color)
        d.text((x0 + 18, y0 + 20), kick, font=f_pkick, fill=color)
        hl = wrap(d, head, f_phead, 340)
        draw_text_block(d, x0 + 18, y0 + 46, hl, f_phead, INK, 32)
        bl = wrap(d, body, f_pbody, 340)
        draw_text_block(d, x0 + 18, y0 + 46 + 32 * len(hl) + 4, bl, f_pbody,
                        (60, 66, 74), 24)
        ix, iy = x0 + pw - 92, y0 + 78
        if icon == "globe":
            icon_globe(d, ix + 30, iy + 22, 30, TEAL)
        elif icon == "trade":
            icon_trade(d, ix - 6, iy - 8, 72, NAVY)
        elif icon == "flags":
            icon_flags(d, ix - 6, iy - 6, 76)
        else:
            icon_shield(d, ix + 30, iy + 22, 32, RED)

    # ---- ticker strip
    tx0, ty0, tx1, ty1 = M, 858, W - M, 922
    d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=8, fill=RED)
    f_tick = font(SANS_B, 22)
    tick = wrap(d, "ALSO TODAY:  Estonia to shut its border with Russia  ·  "
                "Drones hit a Russian cargo ship in the Baltic  ·  Russian "
                "strike on Lviv kills 2, injures 10", f_tick, tx1 - tx0 - 36)
    draw_text_block(d, tx0 + 18, ty0 + 8, tick, f_tick, WHITE, 26)

    # ---- footer
    f_foot = font(SANS, 19)
    d.text((W // 2, 940), "Sources: Al Jazeera · BBC · The Guardian · "
           "Associated Press · Fox News  —  22 November 2026",
           font=f_foot, fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    print(build())
