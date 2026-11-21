#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news infographic (1024x1024 PNG).

Six stories, each verified against a reputable source reporting on
Saturday 21 November 2026. The picture is drawn with Pillow only:
flat colour panels, simple glyphs and wrapped text, so every word
stays legible when the image is shown small.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

SIZE = 1024
PAPER = (250, 246, 238)     # warm off-white
INK = (22, 30, 48)          # dark slate
MUTED = (74, 80, 96)
BAND = (13, 38, 68)         # deep navy masthead
GOLD = (201, 162, 75)
CARD = (255, 255, 255)
CARD_EDGE = (214, 208, 194)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_DATE = font("DejaVuSans-Bold.ttf", 72)
F_KICK = font("DejaVuSans-Bold.ttf", 23)
F_SUB = font("DejaVuSans.ttf", 23)
F_TAG = font("DejaVuSans-Bold.ttf", 18)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_BODY = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 17)

canvas = Image.new("RGB", (SIZE, SIZE), PAPER)
pen = ImageDraw.Draw(canvas)

# ---- masthead ----
pen.rectangle([0, 0, SIZE, 168], fill=BAND)
pen.text((SIZE // 2, 24), "THE WORLD IN ONE IMAGE", font=F_KICK,
         fill=GOLD, anchor="ma")
pen.text((SIZE // 2, 54), "21 NOVEMBER 2026", font=F_DATE,
         fill=(255, 255, 255), anchor="ma")
pen.text((SIZE // 2, 132), "Saturday  •  The day's world news",
         font=F_SUB, fill=(198, 210, 226), anchor="ma")
pen.rectangle([0, 168, SIZE, 174], fill=GOLD)


def wrap_text(text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if pen.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def glyph(cx, cy, kind, colour):
    """A small white pictogram on a coloured disc."""
    r = 32
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    w = (255, 255, 255)
    if kind == "shield":          # Poland / NATO
        pen.polygon([(cx, cy - 20), (cx + 16, cy - 12), (cx + 16, cy + 4),
                     (cx, cy + 20), (cx - 16, cy + 4), (cx - 16, cy - 12)],
                    outline=w, width=3)
        pen.line([cx, cy - 8, cx, cy + 8], fill=w, width=3)
        pen.line([cx - 7, cy, cx + 7, cy], fill=w, width=3)
    elif kind == "rocket":        # Riyadh intercept
        pen.polygon([(cx, cy - 22), (cx + 8, cy - 2), (cx, cy + 12),
                     (cx - 8, cy - 2)], fill=w)
        pen.line([cx - 12, cy + 16, cx + 12, cy + 16], fill=w, width=3)
        pen.line([cx, cy + 12, cx, cy + 22], fill=(255, 190, 60), width=4)
    elif kind == "chart":         # markets
        pen.line([(cx - 20, cy + 16), (cx - 7, cy + 4), (cx + 3, cy + 10),
                  (cx + 20, cy - 14)], fill=w, width=4)
        pen.polygon([(cx + 20, cy - 14), (cx + 11, cy - 14), (cx + 20, cy - 5)],
                    fill=w)
    elif kind == "speech":        # Zelensky / summit fallout
        pen.rounded_rectangle([cx - 20, cy - 16, cx + 20, cy + 8], radius=8,
                              outline=w, width=3)
        pen.polygon([(cx - 8, cy + 8), (cx - 2, cy + 18), (cx + 4, cy + 8)],
                    fill=w)
        for dx in (-11, 0, 11):
            pen.ellipse([cx + dx - 2, cy - 8, cx + dx + 2, cy - 4], fill=w)
    elif kind == "leaf":          # COP31
        pen.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], outline=w, width=3)
        pen.arc([cx - 12, cy - 12, cx + 12, cy + 12], 200, 340, fill=w, width=3)
        pen.line([cx - 12, cy + 7, cx + 12, cy - 7], fill=w, width=3)
    elif kind == "pill":          # cancer trial
        pen.rounded_rectangle([cx - 20, cy - 10, cx + 20, cy + 10], radius=10,
                              outline=w, width=3)
        pen.line([cx - 6, cy - 10, cx + 6, cy + 10], fill=w, width=3)
        pen.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=w)


# (dateline, accent colour, glyph, headline, caption)
STORIES = [
    ("POLAND", (16, 42, 78), "shield",
     "POLAND INVOKES ARTICLE 4 AFTER MISSILES LAND",
     "Two Russian missiles and a drone land in Poland; Warsaw calls "
     "it a provocation and asks NATO for help."),
    ("RIYADH", (120, 30, 90), "rocket",
     "THREE HOUTHI MISSILES SHOT DOWN OVER RIYADH",
     "Saudi defences shoot down three Houthi missiles fired at Riyadh "
     "early on Saturday, the third night running."),
    ("MARKETS", (14, 110, 110), "chart",
     "AI SELL-OFF PUSHES STOCKS INTO CORRECTION",
     "S&P 500 and Dow in correction as the AI rout deepens; Nasdaq "
     "wipes out its 2026 gains; Bitcoin below $60,000."),
    ("KYIV", (178, 34, 34), "speech",
     "ZELENSKY: PUTIN IS A \u2018KILLER\u2019, NOT A FRIEND",
     "After the Shenzhen summit, Trump calls Putin a friend; Zelensky "
     "tells CNN he is a killer."),
    ("ANTALYA", (34, 120, 60), "leaf",
     "COP31 WORKS AN EXTRA DAY AS DEAL STALLS",
     "Climate talks spill into Saturday with no fossil-fuel mention in "
     "the draft; a third text is promised."),
    ("HEALTH", (120, 60, 20), "pill",
     "CANCER PILL MAKES TUMOURS VANISH IN TRIAL",
     "Daraxonrasib leaves tumours undetectable in one in twelve "
     "patients; 77% alive after a year."),
]

# ---- 2 columns x 3 rows of story cards ----
MARGIN, GAP = 24, 20
CARD_W = (SIZE - 2 * MARGIN - GAP) // 2        # 480
CARD_H = 250
TOP = 188
for i, (tag, colour, icon, head, cap) in enumerate(STORIES):
    col, row = i % 2, i // 2
    x = MARGIN + col * (CARD_W + GAP)
    y = TOP + row * (CARD_H + 16)
    pen.rounded_rectangle([x, y, x + CARD_W, y + CARD_H], radius=14,
                          fill=CARD, outline=CARD_EDGE, width=2)
    glyph(x + 50, y + 50, icon, colour)
    pen.text((x + 96, y + 28), tag, font=F_TAG, fill=colour)
    head_lines = wrap_text(head, F_HEAD, CARD_W - 36)
    hy = y + 92
    for line in head_lines[:2]:
        pen.text((x + 18, hy), line, font=F_HEAD, fill=INK)
        hy += 33
    cap_lines = wrap_text(cap, F_BODY, CARD_W - 36)
    cy = hy + 6
    for line in cap_lines[:3]:
        pen.text((x + 18, cy), line, font=F_BODY, fill=MUTED)
        cy += 26

# ---- footer ----
foot_y = TOP + 3 * CARD_H + 2 * 14 + 6
pen.rectangle([0, foot_y, SIZE, SIZE], fill=BAND)
pen.text((SIZE // 2, foot_y + 14),
         "All stories reported on 21 November 2026  •  Sources: AP, Reuters, BBC, Al Jazeera",
         font=F_FOOT, fill=(198, 210, 226), anchor="ma")

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
canvas.save(out_path, optimize=True)
print("saved", out_path)
