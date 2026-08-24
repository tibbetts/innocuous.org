#!/usr/bin/env python3
"""Generate the 1200x630 base canvas that OpenGraph cards are drawn onto.

Why this exists: Hugo's `images.Text` is a *filter*, so it needs an existing
image to draw on, and this repo has no rasteriser and an SVG logo. Rather than
add an image dependency to the build, the canvas is generated once here and the
PNG is committed. Re-run only if the brand colours change.

Pure standard library on purpose — zlib and struct are enough to write a PNG,
and a build asset should not require anyone to install Pillow to reproduce it.

    python3 tools/og/make-base-card.py assets/img/og-base.png
"""

import struct
import sys
import zlib

WIDTH, HEIGHT = 1200, 630

PAGE = (0xF6, 0xF6, 0xF3)        # --page
PANEL = (0xFC, 0xFC, 0xFB)       # --panel
GREEN = (0x1F, 0x5B, 0x3C)       # --green
GREEN_PALE = (0xE7, 0xF1, 0xEA)  # --green-pale
LINE = (0xE7, 0xE7, 0xE0)        # --line

# The card is a panel inset on the page colour, with a green rule down the left
# edge — the same shapes the site uses for a project card, so a shared link
# reads as belonging to the site before any text is drawn on it.
INSET = 40
RULE_W = 14
RADIUS = 28


def blend(bottom, top, alpha):
    return tuple(round(b + (t - b) * alpha) for b, t in zip(bottom, top))


def in_rounded_rect(x, y, x0, y0, x1, y1, r):
    """Coverage of a rounded rect at a pixel centre: 1 inside, 0 outside.

    Corners are sampled rather than analytically integrated — a 2x2 sample is
    enough to keep the radius from looking stair-stepped at this size.
    """
    if not (x0 <= x < x1 and y0 <= y < y1):
        return 0.0
    cx = None
    if x < x0 + r and y < y0 + r:
        cx, cy = x0 + r, y0 + r
    elif x >= x1 - r and y < y0 + r:
        cx, cy = x1 - r, y0 + r
    elif x < x0 + r and y >= y1 - r:
        cx, cy = x0 + r, y1 - r
    elif x >= x1 - r and y >= y1 - r:
        cx, cy = x1 - r, y1 - r
    if cx is None:
        return 1.0
    hits = 0
    for sx in (x + 0.25, x + 0.75):
        for sy in (y + 0.25, y + 0.75):
            if (sx - cx) ** 2 + (sy - cy) ** 2 <= r * r:
                hits += 1
    return hits / 4.0


def build_rows():
    px0, py0 = INSET, INSET
    px1, py1 = WIDTH - INSET, HEIGHT - INSET
    rows = []
    for y in range(HEIGHT):
        row = bytearray()
        for x in range(WIDTH):
            colour = PAGE
            cover = in_rounded_rect(x, y, px0, py0, px1, py1, RADIUS)
            if cover:
                # hairline border, then the panel fill
                edge = in_rounded_rect(x, y, px0 + 1, py0 + 1, px1 - 1, py1 - 1, RADIUS - 1)
                inner = blend(LINE, PANEL, edge)
                # the green rule, and a pale wash behind the headline area
                if px0 <= x < px0 + RULE_W:
                    inner = GREEN
                elif y > py1 - 150:
                    inner = blend(inner, GREEN_PALE, 0.55)
                colour = blend(PAGE, inner, cover)
            row += bytes(colour)
        rows.append(bytes(row))
    return rows


def write_png(path, rows):
    raw = b"".join(b"\x00" + r for r in rows)  # filter type 0 per scanline

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0))  # 8-bit RGB
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/img/og-base.png"
    write_png(out, build_rows())
    print("wrote %s (%dx%d)" % (out, WIDTH, HEIGHT))
