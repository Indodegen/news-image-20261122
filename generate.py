#!/usr/bin/env python3
"""Draw the news-image-20261122 entry: a 1024x1024 newspaper front page
summing up the world news of Sunday 22 November 2026.

Pure PIL (Pillow) + DejaVu/Liberation fonts, no network, no randomness,
no timestamps: running it twice writes a byte-identical PNG.
Every story below was checked against the wires of 22 Nov 2026
(Reuters/AP/AFP/Al Jazeera/Guardian/SCMP/ESPNcricinfo/FIA/Vatican News/
Detiknews/Xinhua/ABC/MSF). The DATE CHECK box names what was left out
because it belongs to an earlier day.

Run:  python3 generate.py [out.png]
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
CARD = (255, 253, 246)
INK = (22, 22, 22)
MUTED = (110, 105, 92)
NAVY = (20, 38, 74)
NAVY_D = (13, 25, 50)
RED = (179, 38, 30)
RED_D = (140, 28, 22)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
SKY = (135, 190, 220)
SEA = (46, 110, 160)
GREEN = (46, 125, 60)
ORANGE = (224, 122, 26)
YELLOW = (242, 201, 60)
WHITE = (255, 255, 255)
LINE = (190, 184, 170)
DARK = (30, 34, 48)
NIGHT = (16, 24, 48)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)


def rrect(d, box, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=3, fill=fill, outline=outline, width=width)


def tag(d, x, y, label, color):
    """Small filled certainty tag; returns width used."""
    f = font(F_SANS_B, 10)
    w = int(d.textlength(label, font=f)) + 10
    rrect(d, [x, y, x + w, y + 14], fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=WHITE)
    return w


# ---------------------------------------------------------------- illustrations
def _stars(d, x0, y0, x1, y1, n=14, seed=7):
    import random
    rnd = random.Random(seed)
    for _ in range(n):
        x = rnd.randint(x0 + 4, x1 - 4)
        y = rnd.randint(y0 + 3, y1 - 4)
        r = rnd.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 200))


def _building(d, x, y, w, h, lit=0.6, seed=3):
    import random
    rnd = random.Random(seed)
    d.rectangle([x, y, x + w, y + h], fill=(38, 44, 66))
    for wy in range(y + 6, y + h - 4, 12):
        for wx in range(x + 5, x + w - 5, 11):
            if rnd.random() < lit:
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(255, 214, 120))


def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 222, 235))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 160, 120))
    cx, cy, r = x + w // 2, y + h // 2 - 6, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 190), outline=NAVY, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=1)
    for gx in (-14, 6):
        d.ellipse([cx + gx - 7, cy - 12, cx + gx + 7, cy + 2], fill=(90, 170, 90))
    d.ellipse([cx - 6, cy + 12, cx + 8, cy + 24], fill=(90, 170, 90))
    d.rectangle([x + 14, y + h - 52, x + 44, y + h - 34], fill=(120, 72, 40))
    d.rectangle([x + w - 46, y + h - 46, x + w - 16, y + h - 34], fill=(90, 90, 110))
    d.polygon([(x + 16, y + h - 52), (x + 30, y + h - 66), (x + 44, y + h - 52)], fill=RED)
    d.polygon([(x + w - 44, y + h - 46), (x + w - 30, y + h - 60), (x + w - 18, y + h - 46)], fill=NAVY)


def ill_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    _stars(d, x, y, x + w, y + h // 2, 16, 11)
    for i, dx in enumerate((18, 62, 108, 150, 196, 240)):
        dy = y + 14 + (i % 3) * 12
        d.line([dx - 7, dy, dx + 7, dy], fill=(255, 210, 110), width=2)
        d.line([dx, dy - 7, dx, dy + 7], fill=(255, 210, 110), width=2)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=RED)
    _building(d, x + 8, y + h - 64, 46, 64, 0.7, 5)
    _building(d, x + 62, y + h - 84, 54, 84, 0.5, 6)
    _building(d, x + 124, y + h - 56, 42, 56, 0.7, 7)
    _building(d, x + 174, y + h - 74, 60, 74, 0.5, 8)
    _building(d, x + 242, y + h - 52, 48, 52, 0.7, 9)
    d.polygon([(x + 200, y + h - 84), (x + 232, y + 22), (x + 246, y + 22)], fill=(255, 240, 180))
    d.ellipse([x + w - 34, y + 10, x + w - 12, y + 32], fill=(255, 120, 60))
    d.polygon([(x + w - 30, y + 30), (x + w - 18, y + 46), (x + w - 34, y + 44)], fill=(255, 120, 60))


def ill_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 20, 44))
    _stars(d, x, y, x + w, y + h // 2, 10, 21)
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(52, 48, 66))
    for bx in (x + 20, x + 90, x + 170, x + 240):
        d.rectangle([bx, y + h - 62, bx + 34, y + h - 30], fill=(120, 116, 132))
        d.rectangle([bx + 8, y + h - 78, bx + 26, y + h - 62], fill=(120, 116, 132))
    for fx, fy, s in ((x + 60, y + 46, 16), (x + 150, y + 30, 22), (x + 230, y + 52, 14)):
        d.polygon([(fx - s, fy + s), (fx, fy - s), (fx + s, fy + s)], fill=(255, 150, 40))
        d.polygon([(fx - s // 2, fy + s), (fx, fy - s // 2), (fx + s // 2, fy + s)], fill=(255, 220, 90))
    d.arc([x + 120, y + 8, x + 190, y + 78], 200, 340, fill=(200, 200, 210), width=3)
    d.line([x + 155, y + 43, x + 155, y + 78], fill=(200, 200, 210), width=3)


def ill_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    d.polygon([(x + 30, y + h - 30), (x + 90, y + h - 30), (x + 120, y + h - 70),
               (x + 170, y + h - 70), (x + 210, y + h - 30), (x + 260, y + h - 30),
               (x + 260, y + h - 12), (x + 30, y + h - 12)], fill=(170, 200, 150))
    d.ellipse([x + 96, y + 14, x + 126, y + 44], fill=RED)
    d.polygon([(x + 96, y + 36), (x + 111, y + 62), (x + 126, y + 36)], fill=RED)
    d.ellipse([x + 104, y + 22, x + 118, y + 36], fill=WHITE)
    d.polygon([(x + 150, y + 30), (x + 210, y + 40), (x + 150, y + 50)], fill=(60, 66, 80))
    d.polygon([(x + 196, y + 40), (x + 232, y + 34), (x + 232, y + 46)], fill=(60, 66, 80))
    for i in range(5):
        d.ellipse([x + 236 + i * 8, y + 36 + i, x + 242 + i * 8, y + 42 + i], fill=(255, 160, 60))
    d.text((x + 12, y + 8), "POLAND", font=font(F_SANS_B, 13), fill=NAVY)


def ill_benghazi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 20, 44))
    _stars(d, x, y, x + w, y + h // 2, 12, 31)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(28, 68, 110))
    for i in range(6):
        d.arc([x + i * 52 - 10, y + h - 30, x + i * 52 + 42, y + h - 6], 200, 340, fill=(140, 190, 230), width=2)
    d.polygon([(x + 70, y + h - 66), (x + 230, y + h - 66), (x + 216, y + h - 34), (x + 84, y + h - 34)], fill=(70, 76, 92))
    d.rectangle([x + 120, y + h - 92, x + 132, y + h - 66], fill=(70, 76, 92))
    d.polygon([(x + 150, y + h - 100), (x + 178, y + h - 78), (x + 150, y + h - 66)], fill=(255, 150, 40))
    d.polygon([(x + 158, y + h - 88), (x + 172, y + h - 76), (x + 158, y + h - 68)], fill=(255, 220, 90))
    d.line([x + 40, y + 26, x + 52, y + 30], fill=(255, 210, 110), width=2)
    d.line([x + 46, y + 20, x + 46, y + 36], fill=(255, 210, 110), width=2)


def ill_hk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    for bx, bh in ((8, 60), (40, 84), (78, 66), (118, 92), (160, 70), (200, 58)):
        d.rectangle([x + bx, y + h - 26 - bh, x + bx + 30, y + h - 26], fill=(90, 110, 140))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 140, 120))
    d.rectangle([x + w // 2 - 26, y + 16, x + w // 2 + 26, y + 62], fill=(200, 60, 50))
    d.rectangle([x + w // 2 - 26, y + 16, x + w // 2 + 26, y + 26], fill=(160, 40, 36))
    d.line([x + w // 2 - 18, y + 44, x + w // 2 - 6, y + 54], fill=WHITE, width=4)
    d.line([x + w // 2 - 6, y + 54, x + w // 2 + 18, y + 30], fill=WHITE, width=4)


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 110))
    d.ellipse([x + 10, y + 10, x + w - 10, y + h - 10], outline=(255, 255, 255), width=3)
    d.rectangle([x + w // 2 - 34, y + h // 2 - 26, x + w // 2 + 34, y + h // 2 + 26], fill=(210, 180, 120))
    for sx in (-16, 0, 16):
        d.rectangle([x + w // 2 + sx - 2, y + 22, x + w // 2 + sx + 2, y + 46], fill=(240, 220, 140))
    d.rectangle([x + w // 2 - 20, y + 18, x + w // 2 + 20, y + 23], fill=(240, 220, 140))
    d.line([x + 30, y + h - 30, x + w - 60, y + 30], fill=(120, 72, 30), width=7)
    d.ellipse([x + w - 52, y + 18, x + w - 36, y + 34], fill=RED)


def ill_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 40, 56))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(70, 70, 86))
    for i in range(8):
        d.rectangle([x + i * 36, y + h - 40, x + i * 36 + 18, y + h - 34], fill=YELLOW if i % 2 == 0 else WHITE)
    d.polygon([(x + 30, y + 46), (x + 90, y + 46), (x + 120, y + 66), (x + 210, y + 66),
               (x + 230, y + 46), (x + 250, y + 66), (x + 250, y + 82), (x + 30, y + 82)], fill=(200, 30, 40))
    d.ellipse([x + 70, y + 78, x + 96, y + 104], fill=(20, 20, 20))
    d.ellipse([x + 196, y + 78, x + 222, y + 104], fill=(20, 20, 20))
    d.rectangle([x + 120, y + 30, x + 170, y + 48], fill=(220, 230, 240))
    for i in range(4):
        for j in range(2):
            d.rectangle([x + 14 + i * 10, y + 8 + j * 10, x + 24 + i * 10, y + 18 + j * 10],
                        fill=(20, 20, 20) if (i + j) % 2 == 0 else WHITE)


def ill_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(244, 190, 120))
    d.ellipse([x + w - 52, y + 10, x + w - 16, y + 46], fill=(255, 220, 140))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(40, 90, 140))
    for i in range(5):
        d.arc([x + i * 56 - 8, y + h - 40, x + i * 56 + 44, y + h - 12], 200, 340, fill=(180, 220, 245), width=2)
    d.polygon([(x + 30, y + h - 74), (x + 250, y + h - 74), (x + 232, y + h - 40), (x + 48, y + h - 40)], fill=(120, 40, 40))
    d.rectangle([x + 60, y + h - 108, x + 90, y + h - 74], fill=(150, 60, 50))
    d.rectangle([x + 170, y + h - 96, x + 186, y + h - 74], fill=(150, 60, 50))
    for fx, fy, s in ((x + 75, y + h - 116, 12), (x + 178, y + h - 104, 10), (x + 130, y + h - 110, 14)):
        d.polygon([(fx - s, fy + s), (fx, fy - s), (fx + s, fy + s)], fill=(255, 150, 40))
        d.polygon([(fx - s // 2, fy + s), (fx, fy - s // 2), (fx + s // 2, fy + s)], fill=(255, 220, 90))
    for sx in (x + 40, x + 110, x + 200):
        d.ellipse([sx, y + 30, sx + 14, y + 44], fill=(90, 90, 100))
        d.ellipse([sx + 4, y + 22, sx + 18, y + 36], fill=(110, 110, 120))


def ill_power(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 56, 74))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(30, 32, 44))
    d.polygon([(x + 60, y + 14), (x + 96, y + 14), (x + 84, y + h - 24), (x + 72, y + h - 24)], fill=(120, 124, 140))
    d.line([x + 40, y + 26, x + 116, y + 26], fill=(120, 124, 140), width=3)
    d.line([x + 30, y + 40, x + 126, y + 40], fill=(120, 124, 140), width=3)
    d.polygon([(x + 190, y + 10), (x + 170, y + 44), (x + 186, y + 44), (x + 164, y + 78),
               (x + 196, y + 78), (x + 210, y + 44), (x + 194, y + 44)], fill=YELLOW)
    for bx in (x + 150, x + 210, x + 250):
        d.rectangle([bx, y + h - 52, bx + 24, y + h - 24], fill=(24, 26, 36))
        d.rectangle([bx + 4, y + h - 46, bx + 10, y + h - 40], fill=(40, 40, 50))
        d.rectangle([bx + 14, y + h - 46, bx + 20, y + h - 40], fill=(40, 40, 50))


def ill_bolsonaro(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 240, 235))
    d.rectangle([x + 20, y + 16, x + w - 20, y + h - 30], fill=WHITE, outline=(200, 200, 200))
    d.rectangle([x + w // 2 - 8, y + 26, x + w // 2 + 8, y + 58], fill=RED)
    d.rectangle([x + w // 2 - 24, y + 42, x + w // 2 + 24, y + 58], fill=RED)
    d.line([x + 34, y + h - 44, x + 80, y + h - 44, x + 100, y + h - 58, x + 120, y + h - 30,
            x + 140, y + h - 44, x + 190, y + h - 44], fill=TEAL, width=3)
    d.rectangle([x + w - 66, y + 20, x + w - 26, y + 44], fill=(0, 150, 60))
    d.polygon([(x + w - 66, y + 20), (x + w - 46, y + 32), (x + w - 66, y + 44)], fill=YELLOW)


def ill_factory(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 214, 196))
    d.rectangle([x + 16, y + h - 56, x + w - 16, y + h - 22], fill=(140, 90, 70))
    d.polygon([(x + 16, y + h - 56), (x + 60, y + h - 84), (x + 104, y + h - 56)], fill=(110, 70, 56))
    d.rectangle([x + w - 52, y + 18, x + w - 36, y + h - 22], fill=(120, 80, 64))
    for fx, fy, s in ((x + 60, y + 40, 18), (x + 120, y + 52, 14), (x + 190, y + 44, 16)):
        d.polygon([(fx - s, fy + s), (fx, fy - s), (fx + s, fy + s)], fill=(255, 150, 40))
        d.polygon([(fx - s // 2, fy + s), (fx, fy - s // 2), (fx + s // 2, fy + s)], fill=(255, 220, 90))
    for sx, sy, r in ((x + 70, y + 12, 10), (x + 100, y + 6, 13), (x + 140, y + 14, 9)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 125))


def ill_boat(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(170, 205, 230))
    d.rectangle([x, y + h - 40, x + w, y + h], fill=(46, 110, 160))
    for i in range(5):
        d.arc([x + i * 56 - 8, y + h - 46, x + i * 56 + 44, y + h - 18], 200, 340, fill=(220, 240, 250), width=2)
    d.polygon([(x + 60, y + h - 66), (x + 220, y + h - 66), (x + 200, y + h - 44), (x + 80, y + h - 44)], fill=(140, 90, 50))
    d.polygon([(x + 60, y + h - 66), (x + 90, y + h - 96), (x + 100, y + h - 66)], fill=(120, 76, 44))
    d.ellipse([x + 200, y + 16, x + 236, y + 52], outline=RED, width=5)
    d.ellipse([x + 212, y + 28, x + 224, y + 40], outline=RED, width=3)
    d.ellipse([x + 40, y + 30, x + 58, y + 48], fill=(255, 220, 140))


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 226, 214))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(160, 150, 130))
    d.rectangle([x + 30, y + 46, x + 170, y + h - 26], fill=WHITE, outline=(150, 150, 150))
    d.rectangle([x + 170, y + 62, x + 220, y + h - 26], fill=(220, 220, 220), outline=(150, 150, 150))
    d.rectangle([x + 78, y + 56, x + 122, y + 66], fill=RED)
    d.rectangle([x + 96, y + 48, x + 104, y + 74], fill=RED)
    d.ellipse([x + 56, y + h - 40, x + 76, y + h - 20], fill=(30, 30, 30))
    d.ellipse([x + 188, y + h - 40, x + 208, y + h - 20], fill=(30, 30, 30))
    for sx, sy, r in ((x + 200, y + 18, 9), (x + 224, y + 10, 12), (x + 244, y + 22, 8)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(130, 130, 135))


def ill_khartoum(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 210, 150))
    d.ellipse([x + w - 56, y + 12, x + w - 20, y + 48], fill=(255, 200, 90))
    for bx, bh in ((10, 50), (52, 70), (100, 56), (150, 80), (200, 62)):
        d.rectangle([x + bx, y + h - 24 - bh, x + bx + 40, y + h - 24], fill=(170, 140, 110))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(140, 110, 80))
    for sx, sy, r in ((x + 60, y + 20, 10), (x + 90, y + 10, 13), (x + 130, y + 22, 9)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(110, 105, 100))
    d.polygon([(x + 150, y + 40), (x + 170, y + 20), (x + 190, y + 40)], fill=(255, 150, 40))


def ill_pope(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 226, 240))
    d.ellipse([x + w // 2 - 52, y + 8, x + w // 2 + 52, y + 76], fill=(190, 170, 130))
    d.rectangle([x + w // 2 - 52, y + 56, x + w // 2 + 52, y + h - 30], fill=(210, 195, 160))
    d.rectangle([x + w // 2 - 6, y - 2, x + w // 2 + 6, y + 14], fill=GOLD)
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(120, 140, 120))
    for i in range(14):
        cx = x + 14 + i * 18
        cy = y + h - 44 + (i % 2) * 8
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(60, 60, 80))
        d.rectangle([cx - 5, cy + 4, cx + 5, cy + 16], fill=(80, 80, 100))


def ill_basket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 200, 140))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(150, 110, 70))
    d.rectangle([x + w - 78, y + 14, x + w - 70, y + h - 30], fill=(200, 200, 200))
    d.ellipse([x + w - 104, y + 22, x + w - 44, y + 46], outline=RED, width=4)
    for i in range(4):
        d.line([x + w - 100 + i * 14, y + 44, x + w - 96 + i * 14, y + 62], fill=RED, width=2)
    d.ellipse([x + 40, y + 30, x + 96, y + 86], fill=(230, 120, 40))
    d.arc([x + 40, y + 30, x + 96, y + 86], 300, 60, fill=(120, 60, 20), width=3)
    d.line([x + 40, y + 58, x + 96, y + 58], fill=(120, 60, 20), width=3)
    d.line([x + 68, y + 30, x + 68, y + 86], fill=(120, 60, 20), width=3)


def ill_denmark(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240))
    d.rectangle([x + 30, y + 14, x + w - 30, y + h - 16], fill=WHITE, outline=(160, 160, 160))
    for i, yy in enumerate((30, 48, 66, 84)):
        d.rectangle([x + 44, y + yy, x + w - 60, y + yy + 5], fill=(150, 150, 155))
    d.ellipse([x + w - 84, y + h - 52, x + w - 44, y + h - 12], outline=RED, width=4)
    d.text((x + w - 72, y + h - 44), "X", font=font(F_SANS_B, 22), fill=RED)
    d.rectangle([x + 44, y + h - 40, x + 84, y + h - 24], fill=RED)
    d.rectangle([x + 44, y + h - 40, x + 84, y + h - 32], fill=WHITE)
    d.rectangle([x + 60, y + h - 40, x + 68, y + h - 24], fill=WHITE)


ILL = {
    "cop31": ill_cop31, "drones": ill_drones, "bahrain": ill_bahrain,
    "poland": ill_poland, "benghazi": ill_benghazi, "hk": ill_hk,
    "cricket": ill_cricket, "f1": ill_f1, "sparta": ill_sparta,
    "power": ill_power, "bolsonaro": ill_bolsonaro, "factory": ill_factory,
    "boat": ill_boat, "gaza": ill_gaza, "khartoum": ill_khartoum,
    "pope": ill_pope, "basket": ill_basket, "denmark": ill_denmark,
}

# ---------------------------------------------------------------- story data
# region: Europe / Middle East / Asia-Pacific / Americas / Africa / Oceania / World
# tag: REPORTED = carried by the day's wires; CLAIM = one side's account;
#      FORECAST = still to happen at press time.
HEROES = [
    dict(n=1, region="World", place="ANTALYA, T\u00dcRKIYE", beat="CLIMATE",
         tag="REPORTED", ill="cop31",
         head="COP31 ends with no deal",
         body=("The EU rejects a final text that never names fossil fuels; the summit "
               "closes two days late with no agreement. No new draft is offered."),
         src="Reuters \u00b7 AP"),
    dict(n=2, region="Europe", place="DYMER, KYIV REGION", beat="WAR",
         tag="REPORTED", ill="drones",
         head="Russia fires 186 drones; block falls in Dymer",
         body=("Air defences down or jam 161 of 186 drones fired overnight. A block "
               "in Dymer falls; up to 14 may be trapped. Six die in the region."),
         src="Ukrainian Air Force \u00b7 Reuters"),
    dict(n=3, region="Middle East", place="MANAMA, BAHRAIN", beat="GULF",
         tag="CLAIM", ill="bahrain",
         head="Iran claims two US radars hit; Bahrain says plant hit, 2 hurt",
         body=("The IRGC says it hit two Patriot radars at Riffa and Awali. Bahrain "
               "says its defences held; a plant in Sitra burned, two hurt."),
         src="Reuters \u00b7 Al Jazeera"),
]

GRID = [
    dict(n=4, region="Europe", place="POLAND", beat="AIRSPACE", tag="REPORTED", ill="poland",
         head="Russian missiles fall inside Poland",
         body="Missiles and a jet drone fall in Poland; NATO: serious violation.",
         src="Reuters"),
    dict(n=5, region="Africa", place="BENGHAZI, LIBYA", beat="SEA WAR", tag="REPORTED", ill="benghazi",
         head="Ukrainian sea drones hit Russian warship",
         body="Russian corvette hit at Benghazi; reports say it sank.",
         src="Libyan officials \u00b7 Reuters"),
    dict(n=6, region="Asia-Pacific", place="HONG KONG", beat="ELECTION", tag="REPORTED", ill="hk",
         head="Hong Kong votes in record numbers",
         body="856 candidates, 723 seats; turnout 98.37% by 5 pm, a record.",
         src="SCMP"),
    dict(n=7, region="Oceania", place="WELLINGTON", beat="CRICKET", tag="REPORTED", ill="cricket",
         head="India declare on 720/9, a record in NZ",
         body="Rahul 136, Pant 128, Gill 98 \u2014 the highest Test total in NZ.",
         src="ESPNcricinfo"),
    dict(n=8, region="Americas", place="LAS VEGAS", beat="FORMULA 1", tag="REPORTED", ill="f1",
         head="Verstappen takes the Las Vegas GP",
         body="Pole to flag in 1:37:59.24; Norris 2nd. His 75th career win.",
         src="FIA"),
    dict(n=9, region="Europe", place="GULF OF FINLAND", beat="SEA", tag="REPORTED", ill="sparta",
         head="Sparta II still burning off Finland",
         body="Hit Saturday, the ship drifts in Finnish waters, still burning.",
         src="Reuters"),
    dict(n=10, region="Asia-Pacific", place="SERANG, INDONESIA", beat="FIRE", tag="REPORTED", ill="factory",
         head="Candy-factory fire kills 3, 36 missing",
         body="A blaze tears through the Cikande plant; three dead, 36 missing.",
         src="Detiknews"),
    dict(n=11, region="Africa", place="BAYELSA, NIGERIA", beat="DISASTER", tag="REPORTED", ill="boat",
         head="Mourners' boat capsizes, 24 dead",
         body="A boat carrying mourners capsizes; at least 24 dead, search goes on.",
         src="AP"),
    dict(n=12, region="Middle East", place="GAZA CITY", beat="CONFLICT", tag="REPORTED", ill="gaza",
         head="Israeli fire kills four in Gaza",
         body="A strike on a food-aid van kills three; a fourth dies elsewhere.",
         src="Al Jazeera"),
    dict(n=13, region="Americas", place="SAN ANTONIO", beat="NBA", tag="REPORTED", ill="basket",
         head="Wembanyama scores 50 as Spurs roll on",
         body="50 points, 19 rebounds, 5 blocks in a 114\u201391 win over New Orleans.",
         src="Reuters"),
]

ALSO = [
    ("Tehran", "Iran begins rolling power cuts", "RFE/RL"),
    ("Bras\u00edlia", "Bolsonaro in intensive care", "Reuters"),
    ("Khartoum", "Drones strike homes near the city", "AP"),
    ("Vatican City", "Pope hosts 1,300 poor guests", "Vatican News"),
    ("Copenhagen", "Denmark expels Russian attach\u00e9", "Guardian"),
    ("Helsinki", "Russian helicopter in Finnish airspace", "MoD"),
    ("Manila", "Chinese bomber turns back off Manila", "Reports"),
    ("Tokyo", "Japan to train live-fire in India, a first", "Reuters"),
    ("Kathmandu", "Nepal PM begins India visit, his first abroad", "IANS"),
    ("Canberra", "Marles: US report on AUKUS subs is wrong", "ABC"),
    ("Seoul", "Education minister resigns after exam leak", "Reuters"),
    ("Tel Aviv", "Eisenkot invites Likud to coalition talks", "Reuters"),
    ("Washington", "FBI probes hack of its crime database", "AP"),
    ("Brussels", "Belgian controllers join Monday strike", "Xinhua"),
    ("Manipur", "Toxic-liquor toll climbs to 19", "Xinhua"),
    ("Melbourne", "70 years since the 1956 Olympics opened", "ABC"),
    ("London", "England beat New Zealand 37\u201312 in rugby", "Reuters"),
    ("Paris", "France beat Argentina to reach the final", "Reuters"),
    ("Turin", "Zverev v Alcaraz, ATP final \u2014 FORECAST", "ATP"),
    ("Liverpool", "Liverpool v Man Utd, 16:30 GMT \u2014 FORECAST", "Sky"),
    ("London", "Arsenal 2\u20132 Newcastle", "BBC"),
    ("Doha", "Iran talks to Qatari mediators", "Al Jazeera"),
    ("Geneva", "UN sets path on killer robots", "Reuters"),
    ("El-Fasher", "MSF: thousands still missing after fall", "MSF"),
    ("New Delhi", "Capital wakes to unhealthy air, AQI 265", "weather.com"),
    ("Riyadh", "Pakistan-Afghanistan talks end in stalemate", "Reuters"),
    ("Venice", "Biennale closes after six months", "ANSA"),
]

REGIONS = ["Europe", "Middle East", "Asia-Pacific", "Americas", "Africa", "Oceania", "World"]
REGION_COLORS = {"Europe": (31, 78, 140), "Middle East": (179, 38, 30),
                 "Asia-Pacific": (200, 130, 20), "Americas": (90, 60, 140),
                 "Africa": (46, 125, 60), "Oceania": (20, 120, 120),
                 "World": (90, 90, 96)}
NUMBERS = [("186", "drones fired at Ukraine"),
           ("161", "downed or jammed"),
           ("2", "US radars Iran claims it hit"),
           ("723", "Hong Kong seats contested"),
           ("720/9", "India\u2019s record Test total"),
           ("50", "Wembanyama points")]
TIMELINE = [("01:00", "HK polls open"), ("03:00", "COP31 objections"),
            ("05:11", "Hamas seeks talks"), ("05:30", "Verstappen wins"),
            ("06:00", "EU rejects text"), ("07:30", "COP31 ends"),
            ("09:45", "Press time")]

TOTAL = len(HEROES) + len(GRID) + len(ALSO)
assert TOTAL == 40, TOTAL


# ---------------------------------------------------------------- layout
def draw_ill(img, key, x, y, w, h):
    """Illustrations are drawn at a fixed 104px design height, then scaled
    to the card's slot, so every card size stays valid."""
    tmp = Image.new("RGB", (w, 104), PAPER)
    td = ImageDraw.Draw(tmp)
    ILL[key](td, 0, 0, w, 104)
    if h != 104:
        tmp = tmp.resize((w, h), Image.LANCZOS)
    img.paste(tmp, (x, y))


def draw_card(img, d, s, x, y, w, h, hero=False):
    rrect(d, [x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    ill_h = 96 if hero else 56
    draw_ill(img, s["ill"], x + 1, y + 1, w - 2, ill_h)
    tag(d, x + 5, y + ill_h - 19, s["tag"],
        RED if s["tag"] == "CLAIM" else (TEAL if s["tag"] == "REPORTED" else NAVY))
    text(d, x + 8, y + ill_h + 5, f"{s['n']}  {s['place']} \u00b7 {s['beat']}",
         font(F_SANS_B, 10), fill=RED_D)
    hf = font(F_SERIF, 21 if hero else 15)
    lh = 23 if hero else 17
    ly = y + ill_h + 19
    for ln in wrap(d, s["head"], hf, w - 16):
        text(d, x + 8, ly, ln, hf)
        ly += lh
    bf = font(F_SANS, 12 if hero else 10)
    blh = 15 if hero else 12
    for ln in wrap(d, s["body"], bf, w - 16):
        if ly + blh > y + h - 14:
            break
        text(d, x + 8, ly, ln, bf)
        ly += blh
    if ly + 4 <= y + h - 13:
        text(d, x + 8, y + h - 13, s["src"], font(F_SANS_I, 9), fill=MUTED)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 22  # margin

    # top bar
    d.rectangle([0, 0, W, 26], fill=NAVY_D)
    text(d, M, 6, "THE WORLD IN ONE DAY", font(F_SANS_B, 13), fill=WHITE)
    right = f"{TOTAL} STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    text(d, W - M, 6, right, font(F_SANS_B, 13), fill=(255, 214, 120), anchor="ra")

    # masthead
    text(d, W // 2, 34, "Sunday 22 November 2026", font(F_SERIF, 66), anchor="ma")
    text(d, W // 2, 108,
         "COP31 ends with no deal \u00b7 186 drones over Ukraine in the night \u00b7 Iran claims US radars hit in Bahrain",
         font(F_SERIF_R, 16), fill=RED_D, anchor="ma")

    # number strip
    y = 132
    cw = (W - 2 * M) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + i * cw
        if i:
            d.line([cx, y + 2, cx, y + 38], fill=LINE, width=1)
        text(d, cx + cw // 2, y, num, font(F_SERIF, 26), fill=RED, anchor="ma")
        for j, ln in enumerate(wrap(d, lab, font(F_SANS, 10), cw - 14)):
            text(d, cx + cw // 2, y + 30 + j * 11, ln, font(F_SANS, 10),
                 fill=MUTED, anchor="ma")

    # region bar
    y = 182
    counts = {r: 0 for r in REGIONS}
    for s in HEROES + GRID:
        counts[s["region"]] += 1
    for i, (place, _, _) in enumerate(ALSO):
        counts[{"Tehran": "Middle East", "Bras\u00edlia": "Americas",
                "Khartoum": "Africa", "Vatican City": "Europe",
                "Copenhagen": "Europe", "Helsinki": "Europe",
                "Manila": "Asia-Pacific", "Tokyo": "Asia-Pacific",
                "Kathmandu": "Asia-Pacific", "Canberra": "Oceania", "Seoul": "Asia-Pacific",
                "Tel Aviv": "Middle East", "Washington": "Americas", "Brussels": "Europe",
                "Manipur": "Asia-Pacific", "Melbourne": "Oceania", "London": "Europe",
                "Paris": "Europe", "Turin": "Europe", "Liverpool": "Europe",
                "Doha": "Middle East", "Geneva": "Europe", "El-Fasher": "Africa",
                "New Delhi": "Asia-Pacific", "Riyadh": "Middle East",
                "Venice": "Europe"}[place]] += 1
    assert sum(counts.values()) == TOTAL, counts
    bx = M
    seg = (W - 2 * M) // len(REGIONS)
    for i, r in enumerate(REGIONS):
        d.rectangle([bx, y, bx + seg - 1, y + 18], fill=REGION_COLORS[r])
        text(d, bx + seg // 2, y + 4, f"{r.upper()} {counts[r]}",
             font(F_SANS_B, 10), fill=WHITE, anchor="ma")
        bx += seg

    # timeline
    y = 206
    text(d, M, y, "THE DAY IN UTC", font(F_SANS_B, 11), fill=NAVY)
    tx = M + 108
    for t, lab in TIMELINE:
        text(d, tx, y, t, font(F_SANS_B, 11), fill=RED_D)
        tx += int(d.textlength(t, font=font(F_SANS_B, 11))) + 5
        text(d, tx, y, lab, font(F_SANS, 11))
        tx += int(d.textlength(lab, font=font(F_SANS, 11))) + 12

    # hero row
    y = 226
    hh = 210
    hw = (W - 2 * M - 16) // 3
    for i, s in enumerate(HEROES):
        draw_card(img, d, s, M + i * (hw + 8), y, hw, hh, hero=True)

    # grid rows (5 across, 2 rows)
    y = 444
    gh = 150
    gw = (W - 2 * M - 4 * 8) // 5
    for row in range(2):
        for col in range(5):
            s = GRID[row * 5 + col]
            draw_card(img, d, s, M + col * (gw + 8), y + row * (gh + 8), gw, gh)

    # bottom: map + also list
    y = 760
    d.line([M, y, W - M, y], fill=NAVY, width=2)
    text(d, M, y + 5, "WHERE IT HAPPENED", font(F_SANS_B, 11), fill=NAVY)
    text(d, M + 300, y + 5, f"ALSO ON SUNDAY 22 NOVEMBER \u2014 {len(ALSO)} MORE STORIES",
         font(F_SANS_B, 11), fill=NAVY)
    map_x, map_y, map_w, map_h = M, y + 22, 280, 130
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(214, 228, 240),
                outline=LINE)
    _draw_map(d, map_x, map_y, map_w, map_h)
    ax = M + 300
    col_w = (W - M - ax - 8) // 2
    af = font(F_SANS, 10)
    for i, (place, head, src) in enumerate(ALSO):
        line = f"{14 + i}. {place} \u2014 {head} ({src})"
        assert d.textlength(line, font=af) <= col_w - 11, f"ALSO overflow: {line}"
        cx = ax + (i // 14) * (col_w + 8)
        cy = y + 22 + (i % 14) * 10
        n = 14 + i
        d.rectangle([cx, cy + 2, cx + 6, cy + 8], fill=RED)
        text(d, cx + 11, cy, line, af)

    # date check
    y = 930
    d.rectangle([M, y, W - M, y + 54], outline=RED, width=2)
    text(d, M + 6, y + 4, "DATE CHECK \u2014 READ THIS FIRST",
         font(F_SANS_B, 11), fill=RED)
    dc = ("Every story above happened, or was first reported, on Sunday 22 November 2026 "
          "(UTC), to press time 09:45 UTC. Left out because they belong to an earlier day: "
          "the Peru quake (Fri 20 Nov, USGS 6.7) \u00b7 the Myanmar genocide ruling (Thu 19 Nov) "
          "\u00b7 the Shenzhen summit (Thu\u2013Fri 19\u201320 Nov) \u00b7 \u2018El Chapo Isidro\u2019 arrested "
          "(Fri 20 Nov) \u00b7 BepiColombo reaches Mercury (Sat 21 Nov) \u00b7 the Nvidia SEC probe "
          "(Fri 20 Nov) \u00b7 the Kryvyi Rih strike (Sat 21 Nov; its toll was reported Sunday). "
          "The Sparta II was hit on Saturday \u2014 it is counted because it was still burning on "
          "Sunday. The COP31 draft landed on Saturday; its collapse is Sunday\u2019s news.")
    for j, ln in enumerate(wrap(d, dc, font(F_SANS, 10), W - 2 * M - 12)):
        text(d, M + 6, y + 17 + j * 10, ln, font(F_SANS, 10))

    # footer
    text(d, M, H - 12,
         "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 Guardian \u00b7 SCMP \u00b7 ESPNcricinfo \u00b7 FIA \u00b7 Vatican News \u00b7 Detiknews \u00b7 Xinhua \u00b7 ABC \u00b7 MSF \u2014 scenes drawn, not photographs.",
         font(F_SANS, 9), fill=MUTED)
    text(d, W - M, H - 12,
         "REPORTED = wires \u00b7 CLAIM = one side \u00b7 FORECAST = yet to happen",
         font(F_SANS, 9), fill=MUTED, anchor="ra")

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


def _draw_map(d, x, y, w, h):
    """Dot-matrix world map from a coarse land mask, with red pins at the
    featured stories' longitudes/latitudes."""
    cols, rows = 56, 24
    cw, ch = w / cols, h / rows
    land = [
        (0, 2, 16), (0, 18, 22), (0, 36, 54),
        (1, 1, 17), (1, 34, 55),
        (2, 1, 18), (2, 26, 33), (2, 34, 55),
        (3, 2, 18), (3, 25, 33), (3, 34, 55),
        (4, 3, 17), (4, 25, 33), (4, 35, 54),
        (5, 4, 16), (5, 25, 32), (5, 36, 53),
        (6, 5, 15), (6, 25, 32), (6, 37, 52),
        (7, 6, 14), (7, 25, 33), (7, 38, 51),
        (8, 7, 13), (8, 27, 33), (8, 39, 50),
        (9, 8, 12), (9, 28, 33), (9, 40, 49),
        (10, 8, 11), (10, 29, 32), (10, 41, 47),
        (11, 9, 11), (11, 15, 20), (11, 29, 31), (11, 42, 46),
        (12, 15, 20), (12, 30, 31), (12, 44, 46),
        (13, 15, 20), (13, 47, 49),
        (14, 16, 20), (14, 45, 50),
        (15, 16, 19), (15, 44, 50),
        (16, 16, 19), (16, 44, 50),
        (17, 17, 19), (17, 44, 50),
        (18, 17, 18), (18, 45, 49),
        (19, 17, 18), (19, 46, 48),
        (20, 17, 18), (20, 46, 47),
        (21, 17, 18),
        (22, 18, 18),
        (23, 18, 18),
    ]
    for r, c0, c1 in land:
        for c in range(c0, c1 + 1):
            cx = x + c * cw + cw / 2
            cy = y + r * ch + ch / 2
            d.ellipse([cx - 1.6, cy - 1.6, cx + 1.6, cy + 1.6], fill=(198, 182, 148))
    pins = [(30.7, 36.9), (30.5, 50.5), (50.6, 26.2), (19.4, 52.0),
            (20.1, 32.1), (114.2, 22.3), (174.8, -41.3), (-115.1, 36.2),
            (24.0, 59.9), (106.1, -6.1), (6.0, 4.8), (34.5, 31.5),
            (-98.5, 29.4)]
    for lon, lat in pins:
        px = x + (lon + 170) / 360 * w
        py = y + (75 - lat) / 130 * h
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED, outline=WHITE, width=1)
    text(d, x + 4, y + h - 11, "Dot map \u2014 red dots mark the featured stories.",
         font(F_SANS, 8), fill=MUTED)


if __name__ == "__main__":
    main()
