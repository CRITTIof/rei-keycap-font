"""Shared geometry for the tight keycaps.

Design coordinates: x grows right, y grows down.  The key box is 62 px tall.
The font maps this to 1000 units/em with the box filling the em.
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # project root
OUT = ROOT / "fonts"                                # generated fonts

from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

from data import ICONS, ALL_KEYCAPS, ALL_GLYPHS, PUA

FONT_SRC = ROOT / "assets" / "noto-sans-semibold.ttf"
MONO_SRC = ROOT / "assets" / "jetbrains-mono-semibold.ttf"


def load_face(path):
    font = TTFont(path)
    return {
        "font": font,
        "glyphs": font.getGlyphSet(),
        "cmap": font.getBestCmap(),
        "hmtx": font["hmtx"],
        "upem": font["head"].unitsPerEm,
    }


SANS = load_face(FONT_SRC)
MONO = load_face(MONO_SRC)
FACES = {"sans": SANS, "mono": MONO}

# Backwards-compatible aliases for the proportional face.
SRC = SANS["font"]
GLYPHS = SANS["glyphs"]
CMAP = SANS["cmap"]
HMTX = SANS["hmtx"]
UPEM = SANS["upem"]

FONT_SIZE = 42.0
SCALE = FONT_SIZE / UPEM
PAD_X = 20.0
BOX_H = 62.0
STROKE = 4.0
RADIUS_OUT = 16.0
RADIUS_IN = 12.0
K = 0.5522847498307936

ARROW_W = 58.0
ARROW_ANGLE = {"up": 0.0, "right": 90.0, "down": 180.0, "left": 270.0}

ICON_W = 62.0
ICON_H = 62.0
ICON_STROKE = 3.5

META = {}
for gid, label, full, group in ALL_KEYCAPS:
    META[gid] = {"label": label, "full": full, "group": group,
                 "pua": PUA[gid], "kind": "keycap"}
for gid, label, full, group in ICONS:
    META[gid] = {"label": label, "full": full, "group": group,
                 "pua": PUA[gid], "kind": "icon"}

# Normal-text aliases for the 26 letters and 10 digits.  Both cases map to the
# same uppercase keycap so `A` and `a` both render the A key.
TEXT_CHARS = {}
TEXT_CMAP = {}
for gid, label, full, group in ALL_KEYCAPS:
    if len(label) != 1 or not label.isascii():
        continue
    if label.isalpha():
        chars = [label, label.lower()]
    elif label.isdigit():
        chars = [label]
    else:
        continue
    TEXT_CHARS[gid] = chars
    for ch in chars:
        TEXT_CMAP[ord(ch)] = gid

assert len(TEXT_CMAP) == 62, len(TEXT_CMAP)

# Windows-safe, human-readable folder names.  A few key legends are illegal
# filename characters, so they get a descriptive word instead.
FOLDER_LABEL = {
    "\\": "Backslash",
    "/": "Slash",
    "*": "Asterisk",
    "+": "Plus",
    "`": "Backquote",
    "-": "Minus",
    "=": "Equal",
    "[": "BracketLeft",
    "]": "BracketRight",
    ";": "Semicolon",
    "'": "Apostrophe",
    ",": "Comma",
    ".": "Period",
    "←": "ArrowLeft",
    "↑": "ArrowUp",
    "↓": "ArrowDown",
    "→": "ArrowRight",
}


def folder_name(gid):
    """Stable per-character folder, e.g. U+E000_Esc or U+E01E_Backslash."""
    meta = META[gid]
    label = FOLDER_LABEL.get(meta["label"], meta["label"])
    label = "".join(c if c.isalnum() or c in "._-" else "_" for c in label)
    return f"U+{meta['pua']:04X}_{label}"

FONT_UPEM = 1000
FONT_SCALE = FONT_UPEM / BOX_H
SIDE_BEARING = 16


def is_arrow(gid):
    return gid.startswith("arrow")


def arrow_points(direction, w=ARROW_W, h=BOX_H):
    cx, cy = w / 2, h / 2
    pts = [
        (-2.25, 18.5), (-2.25, 0.5), (-9.0, 0.5),
        (0.0, -18.5), (9.0, 0.5), (2.25, 0.5), (2.25, 18.5),
    ]
    a = math.radians(ARROW_ANGLE[direction])
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + x * ca - y * sa, cy + x * sa + y * ca) for x, y in pts]


def face_for_label(label):
    """Letters and digits use a monospaced face, so every one has one width."""
    if len(label) == 1 and label.isascii() and label.isalnum():
        return "mono"
    return "sans"


def text_width(label, face="sans"):
    f = FACES[face]
    scale = FONT_SIZE / f["upem"]
    return sum(f["hmtx"][f["cmap"][ord(c)]][0] * scale for c in label)


def text_bounds(label, face="sans"):
    f = FACES[face]
    scale = FONT_SIZE / f["upem"]
    pen = BoundsPen(f["glyphs"])
    x = 0.0
    for c in label:
        gn = f["cmap"][ord(c)]
        f["glyphs"][gn].draw(TransformPen(pen, (scale, 0, 0, scale, x, 0)))
        x += f["hmtx"][gn][0] * scale
    return pen.bounds


def text_run_width(label, face, size):
    f = FACES[face]
    scale = size / f["upem"]
    return sum(f["hmtx"][f["cmap"][ord(c)]][0] * scale for c in label)


def draw_text_run(pen, label, face, size, x, baseline):
    """Draw a y-down text run, used inside the pictogram design box."""
    f = FACES[face]
    scale = size / f["upem"]
    for c in label:
        gn = f["cmap"][ord(c)]
        f["glyphs"][gn].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        x += f["hmtx"][gn][0] * scale


def design_for(gid):
    if META[gid]["kind"] == "icon":
        return {"W": ICON_W, "H": ICON_H, "kind": "icon"}
    label = META[gid]["label"]
    if is_arrow(gid):
        return {
            "W": ARROW_W,
            "tw": 18.0,
            "baseline": BOX_H / 2,
            "kind": "arrow",
            "direction": gid[5:],
        }
    face = face_for_label(label)
    tw = text_width(label, face)
    W = tw + 2 * PAD_X
    b = text_bounds(label, face)
    ymin, ymax = b[1], b[3]
    baseline = BOX_H / 2 + (ymin + ymax) / 2
    return {"W": W, "tw": tw, "baseline": baseline, "kind": "text",
            "label": label, "face": face}


def rr(pen, x, y, w, h, r):
    """Clockwise rounded rectangle in y-down coordinates."""
    pen.moveTo((x + r, y))
    pen.lineTo((x + w - r, y))
    pen.curveTo((x + w - r + K * r, y), (x + w, y + r - K * r), (x + w, y + r))
    pen.lineTo((x + w, y + h - r))
    pen.curveTo((x + w, y + h - r + K * r), (x + w - r + K * r, y + h), (x + w - r, y + h))
    pen.lineTo((x + r, y + h))
    pen.curveTo((x + r - K * r, y + h), (x, y + h - r + K * r), (x, y + h - r))
    pen.lineTo((x, y + r))
    pen.curveTo((x, y + r - K * r), (x + r - K * r, y), (x + r, y))
    pen.closePath()


def arc(pen, cx, cy, r, a0, a1):
    """Cubic approximation of a positive (counter-clockwise in math coords)
    arc.  Coordinates are y-down, so this appears clockwise on screen."""
    steps = max(1, int(math.ceil((a1 - a0) / (math.pi / 2))))
    for i in range(steps):
        t0 = a0 + (a1 - a0) * i / steps
        t1 = a0 + (a1 - a0) * (i + 1) / steps
        delta = t1 - t0
        k = (4.0 / 3.0) * math.tan(delta / 4.0) * r
        p0 = (cx + r * math.cos(t0), cy + r * math.sin(t0))
        p3 = (cx + r * math.cos(t1), cy + r * math.sin(t1))
        p1 = (p0[0] - k * math.sin(t0), p0[1] + k * math.cos(t0))
        p2 = (p3[0] + k * math.sin(t1), p3[1] - k * math.cos(t1))
        pen.curveTo(p1, p2, p3)


def circle(pen, cx, cy, r):
    """Filled circle, same winding as rr()."""
    pen.moveTo((cx + r, cy))
    arc(pen, cx, cy, r, 0, 2 * math.pi)
    pen.closePath()


def ellipse(pen, cx, cy, rx, ry):
    """Filled ellipse, same winding as circle()."""
    pen.moveTo((cx + rx, cy))
    pen.curveTo((cx + rx, cy + ry * K), (cx + rx * K, cy + ry), (cx, cy + ry))
    pen.curveTo((cx - rx * K, cy + ry), (cx - rx, cy + ry * K), (cx - rx, cy))
    pen.curveTo((cx - rx, cy - ry * K), (cx - rx * K, cy - ry), (cx, cy - ry))
    pen.curveTo((cx + rx * K, cy - ry), (cx + rx, cy - ry * K), (cx + rx, cy))
    pen.closePath()


def capsule(pen, x1, y1, x2, y2, w=ICON_STROKE):
    """A line segment with round caps, expanded to a filled outline."""
    r = w / 2.0
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length < 1e-9:
        circle(pen, x1, y1, r)
        return
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux
    a = math.atan2(uy, ux)
    p1b = (x1 - nx * r, y1 - ny * r)
    p2b = (x2 - nx * r, y2 - ny * r)
    p1a = (x1 + nx * r, y1 + ny * r)
    p2a = (x2 + nx * r, y2 + ny * r)
    pen.moveTo(p1b)
    pen.lineTo(p2b)
    arc(pen, x2, y2, r, a - math.pi / 2, a + math.pi / 2)
    pen.lineTo(p1a)
    arc(pen, x1, y1, r, a + math.pi / 2, a + 3 * math.pi / 2)
    pen.closePath()


def poly_round(pen, pts, r):
    """Filled polygon whose corners are rounded with radius ``r``."""
    n = len(pts)

    def unit(dx, dy):
        length = math.hypot(dx, dy)
        return (dx / length, dy / length) if length > 1e-9 else (0.0, 0.0)

    for i in range(n):
        prev, cur, nxt = pts[(i - 1) % n], pts[i], pts[(i + 1) % n]
        # Never eat more than half of either adjacent edge.
        room = min(math.hypot(prev[0] - cur[0], prev[1] - cur[1]),
                   math.hypot(nxt[0] - cur[0], nxt[1] - cur[1])) * 0.5
        rr_ = min(r, room)
        u1 = unit(prev[0] - cur[0], prev[1] - cur[1])
        u2 = unit(nxt[0] - cur[0], nxt[1] - cur[1])
        p1 = (cur[0] + u1[0] * rr_, cur[1] + u1[1] * rr_)
        p2 = (cur[0] + u2[0] * rr_, cur[1] + u2[1] * rr_)
        if i == 0:
            pen.moveTo(p1)
        else:
            pen.lineTo(p1)
        pen.curveTo((p1[0] + (cur[0] - p1[0]) * K, p1[1] + (cur[1] - p1[1]) * K),
                    (p2[0] + (cur[0] - p2[0]) * K, p2[1] + (cur[1] - p2[1]) * K),
                    p2)
    pen.closePath()


def stroke_arc(pen, cx, cy, r, a0, a1, w=ICON_STROKE, steps=None):
    """Approximate a round-capped circular arc with overlapping capsules."""
    if steps is None:
        steps = max(2, int(math.ceil(abs(a1 - a0) / (math.pi / 36))))
    prev = (cx + r * math.cos(a0), cy + r * math.sin(a0))
    for i in range(1, steps + 1):
        t = a0 + (a1 - a0) * i / steps
        p = (cx + r * math.cos(t), cy + r * math.sin(t))
        capsule(pen, prev[0], prev[1], p[0], p[1], w)
        prev = p


def ring_rr(pen, x, y, w, h, r, stroke=ICON_STROKE):
    s = stroke
    rr(pen, x - s / 2, y - s / 2, w + s, h + s, r + s / 2)
    inner = ReverseContourPen(pen)
    rr(inner, x + s / 2, y + s / 2, w - s, h - s, max(0.1, r - s / 2))


def ring_circle(pen, cx, cy, r, stroke=ICON_STROKE):
    s = stroke
    circle(pen, cx, cy, r + s / 2)
    circle(ReverseContourPen(pen), cx, cy, max(0.1, r - s / 2))


def ring_ellipse(pen, cx, cy, rx, ry, stroke=ICON_STROKE):
    s = stroke
    ellipse(pen, cx, cy, rx + s / 2, ry + s / 2)
    ellipse(ReverseContourPen(pen), cx, cy,
            max(0.1, rx - s / 2), max(0.1, ry - s / 2))


def draw_app_frame(pen, gap_y=34.0, stroke=ICON_STROKE):
    """Rounded app tile with the lower-right border opened for the label.

    The opening removes the right side below ``gap_y`` and the whole
    bottom-right corner, so a large APP label can spill over the tile edge
    without ever touching the frame.
    """
    x0, y0, x1, y1, r = 6, 7, 56, 57, 10
    capsule(pen, x0 + r, y0, x1 - r, y0, stroke)
    capsule(pen, x0, y0 + r, x0, y1 - r, stroke)
    capsule(pen, x0 + r, y1, x1 - r, y1, stroke)
    capsule(pen, x1, y0 + r, x1, gap_y, stroke)
    stroke_arc(pen, x0 + r, y0 + r, r, math.pi, 1.5 * math.pi, stroke)
    stroke_arc(pen, x1 - r, y0 + r, r, -0.5 * math.pi, 0.0, stroke)
    stroke_arc(pen, x0 + r, y1 - r, r, 0.5 * math.pi, math.pi, stroke)


def draw_icon_svg(pen, gid):
    """Filled line-art outlines for the system pictograms.

    All coordinates live in a 62 x 62 design box.  The shapes are built from
    capsules, rings and dots so the same path can be used by SVG and by the
    font (fonts can only fill, not stroke).
    """
    if gid == "cpu":
        ring_rr(pen, 13, 13, 36, 36, 5)
        ring_rr(pen, 25, 25, 12, 12, 2)
        # Pins end at y=8/54 so every hardware icon shares the same
        # 46-unit visual height.
        for p in (22, 31, 40):
            capsule(pen, p, 9.75, p, 14)
            capsule(pen, p, 48, p, 52.25)
            capsule(pen, 9.75, p, 14, p)
            capsule(pen, 48, p, 52.25, p)

    elif gid == "gpu":
        # Taller card: the three bottom pins keep their spacing and width.
        ring_rr(pen, 11, 10, 39, 36, 4)
        capsule(pen, 5.5, 9.6, 5.5, 46, 3.2)
        capsule(pen, 3.6, 13, 7.4, 13, 3.0)
        capsule(pen, 3.6, 43, 7.4, 43, 3.0)
        ring_ellipse(pen, 31, 28, 7.2, 7.2, 3.0)
        for x in (19, 30.5, 42):
            capsule(pen, x, 46, x, 52.8, 2.4)

    elif gid == "ram":
        # Full-height module: four vertical chips and five bottom pins.
        ring_rr(pen, 6, 9.75, 50, 33.5, 3)
        for x in (11.5, 22.5, 33.5, 44.5):
            ring_rr(pen, x, 17.5, 8, 18, 1.2, 2.2)
        for x in (12, 21, 30, 39, 48):
            capsule(pen, x, 44, x, 52.8, 2.4)

    elif gid == "rom":
        # "ROM" in this keyboard means the hard drive: enclosure, platter,
        # spindle and actuator arm.
        ring_rr(pen, 7, 9.75, 48, 42.5, 4)
        ring_circle(pen, 24, 30, 12.0, 3.2)
        circle(pen, 24, 30, 2.5)
        circle(pen, 47, 17, 2.4)
        capsule(pen, 47, 17, 30, 27, 3.0)

    elif gid == "terminal":
        ring_rr(pen, 8, 14, 46, 34, 4)
        capsule(pen, 12, 23, 50, 23, 2.2)
        capsule(pen, 15, 30, 21, 35, 2.6)
        capsule(pen, 21, 35, 15, 40, 2.6)
        capsule(pen, 26, 40, 34, 40, 2.8)

    elif gid == "web":
        ring_rr(pen, 8, 14, 46, 34, 4)
        capsule(pen, 12, 23, 50, 23, 2.2)
        capsule(pen, 22, 32, 42, 32, 2.8)
        capsule(pen, 22, 40, 42, 40, 2.8)

    elif gid == "app":
        # Large APP label at the lower-right; the frame opens behind it.
        draw_app_frame(pen, gap_y=33.0)
        label = "APP"
        size = 25.5
        draw_text_run(pen, label, "mono", size, 16.0, 54.0)

    elif gid == "game":
        ring_rr(pen, 8, 21, 46, 22, 9)
        capsule(pen, 16, 32, 26, 32, 2.6)
        capsule(pen, 21, 27, 21, 37, 2.6)
        for cx, cy in ((40, 28), (44, 32), (40, 36), (36, 32)):
            circle(pen, cx, cy, 1.8)

    elif gid == "usb":
        # Front view of a USB-A flash drive: metal plug with two square
        # cut-outs, then a slightly wider body with an open bottom.
        ring_rr(pen, 17, 9.75, 28, 22, 2.5)
        ring_rr(pen, 22.0, 16.25, 5.2, 5.2, 0.8, 2.2)
        ring_rr(pen, 34.8, 16.25, 5.2, 5.2, 0.8, 2.2)
        capsule(pen, 42.8, 10.35, 42.8, 31.15, 1.6)
        capsule(pen, 15.5, 32.25, 15.5, 52.25, 3.5)
        capsule(pen, 46.5, 32.25, 46.5, 52.25, 3.5)

    elif gid == "volume":
        ring_rr(pen, 9, 18.5, 11, 25, 2, 3.0)
        capsule(pen, 20, 18.5, 36, 9.5, 3.0)
        capsule(pen, 36, 9.5, 36, 52.5, 3.0)
        capsule(pen, 20, 43.5, 36, 52.5, 3.0)
        stroke_arc(pen, 36, 31, 10.5, math.radians(-55), math.radians(55), 2.6)
        stroke_arc(pen, 36, 31, 16.0, math.radians(-55), math.radians(55), 2.6)

    elif gid == "folder":
        # Folder with a tab and a front-panel fold line.
        capsule(pen, 10, 18, 25, 18)
        capsule(pen, 25, 18, 31, 24)
        capsule(pen, 31, 24, 50, 24)
        capsule(pen, 50, 24, 50, 48)
        capsule(pen, 50, 48, 12, 48)
        capsule(pen, 12, 48, 12, 18)
        capsule(pen, 10, 31, 52, 31, 2.8)

    elif gid == "txt":
        # Text document with a folded top-right corner and three text lines.
        capsule(pen, 15, 10, 38, 10)
        capsule(pen, 38, 10, 47, 19)
        capsule(pen, 47, 19, 47, 50)
        capsule(pen, 47, 50, 15, 50)
        capsule(pen, 15, 50, 15, 10)
        capsule(pen, 38, 10, 38, 19, 3.0)
        capsule(pen, 38, 19, 47, 19, 3.0)
        for y, w in ((26, 26), (34, 26), (42, 17)):
            capsule(pen, 21, y, 21 + w, y, 2.8)

    elif gid == "agent":
        # AI agent: robot head with antenna, side sensors, eyes and mouth.
        capsule(pen, 31, 19, 31, 13, 3.0)
        circle(pen, 31, 11.2, 2.2)
        ring_rr(pen, 12, 19, 38, 29, 7)
        capsule(pen, 9, 29, 9, 39, 3.0)
        capsule(pen, 53, 29, 53, 39, 3.0)
        circle(pen, 24, 31, 2.2)
        circle(pen, 38, 31, 2.2)
        capsule(pen, 25, 40, 37, 40, 2.8)

    elif gid == "image":
        # Picture frame with a sun and two mountain peaks.
        ring_rr(pen, 8, 12, 46, 38, 4)
        circle(pen, 21, 24, 3.2)
        capsule(pen, 13, 43, 26, 29, 3.0)
        capsule(pen, 26, 29, 34, 38, 3.0)
        capsule(pen, 34, 38, 42, 29, 3.0)
        capsule(pen, 42, 29, 50, 38, 3.0)

    elif gid == "microphone":
        # Microphone capsule, U-shaped cradle, stem and base.
        ring_rr(pen, 24, 9.5, 14, 27, 7)
        stroke_arc(pen, 31, 34, 11.5, 0.0, math.pi, 3.2)
        capsule(pen, 31, 45, 31, 50)
        capsule(pen, 23, 52.25, 39, 52.25, 3.4)

    elif gid == "content":
        # Text block: one heavy heading bar above three body lines.
        capsule(pen, 13, 14, 49, 14, 4.6)
        capsule(pen, 13, 26.5, 49, 26.5, 2.8)
        capsule(pen, 13, 37, 41, 37, 2.8)
        capsule(pen, 13, 47.5, 34, 47.5, 2.8)

    elif gid == "appearance":
        # Paint palette: tray with a thumb notch and three paint dots.  The
        # rim gap matches the notch so the circle reads as a cut-out.
        stroke_arc(pen, 31, 31, 20.5, math.radians(64.7), math.radians(385.3), 3.4)
        ring_circle(pen, 45.5, 45.5, 7.0, 3.4)
        circle(pen, 21, 30, 2.5)
        circle(pen, 25.5, 21, 2.5)
        circle(pen, 34, 17.5, 2.5)

    elif gid == "datasource":
        # Database cylinder: top disk, two body bands and two side walls.
        ring_ellipse(pen, 31, 15.5, 17, 5.6, 3.2)
        capsule(pen, 14, 15.5, 14, 46.5, 3.2)
        capsule(pen, 48, 15.5, 48, 46.5, 3.2)
        ring_ellipse(pen, 31, 31, 17, 5.6, 2.6)
        ring_ellipse(pen, 31, 46.5, 17, 5.6, 2.6)

    elif gid == "behavior":
        # Mouse pointer, the universal "action" mark.
        pts = [
            (18, 11), (18, 44), (26, 36), (31, 47), (36.2, 44.6),
            (31.2, 34), (41, 34),
        ]
        pen.moveTo(pts[0])
        for p in pts[1:]:
            pen.lineTo(p)
        pen.closePath()

    elif gid == "search":
        # Magnifier: lens ring with a diagonal handle.
        ring_circle(pen, 25, 24, 13, 3.4)
        capsule(pen, 34.2, 33.2, 48.5, 47.5, 4.4)

    elif gid == "hotkey":
        # Keycap outline with a bolt: a keyboard shortcut.
        ring_rr(pen, 9, 13, 44, 36, 7)
        bolt = [
            (33.5, 18.5), (23.5, 33), (29.5, 33), (27, 43.5),
            (38, 29), (32, 29),
        ]
        pen.moveTo(bolt[0])
        for p in bolt[1:]:
            pen.lineTo(p)
        pen.closePath()

    elif gid == "trash":
        # Waste bin: lid, handle, tapered body and two ribs.
        capsule(pen, 13, 16, 49, 16, 4.2)
        capsule(pen, 25.5, 11, 36.5, 11, 3.4)
        capsule(pen, 25.5, 12, 25.5, 15.5, 3.0)
        capsule(pen, 36.5, 12, 36.5, 15.5, 3.0)
        capsule(pen, 17.5, 18.5, 20.5, 50, 3.4)
        capsule(pen, 44.5, 18.5, 41.5, 50, 3.4)
        capsule(pen, 20.5, 50, 41.5, 50, 3.4)
        capsule(pen, 27, 25, 27, 43.5, 2.6)
        capsule(pen, 35, 25, 35, 43.5, 2.6)

    elif gid == "move":
        # Four-way arrow cross.
        capsule(pen, 31, 13, 31, 49, 3.4)
        capsule(pen, 13, 31, 49, 31, 3.4)
        capsule(pen, 31, 12, 25.8, 19, 3.4)
        capsule(pen, 31, 12, 36.2, 19, 3.4)
        capsule(pen, 31, 50, 25.8, 43, 3.4)
        capsule(pen, 31, 50, 36.2, 43, 3.4)
        capsule(pen, 12, 31, 19, 25.8, 3.4)
        capsule(pen, 12, 31, 19, 36.2, 3.4)
        capsule(pen, 50, 31, 43, 25.8, 3.4)
        capsule(pen, 50, 31, 43, 36.2, 3.4)

    elif gid == "add":
        # Plus sign.
        capsule(pen, 31, 15, 31, 47, 4.4)
        capsule(pen, 15, 31, 47, 31, 4.4)

    elif gid == "expand":
        # Two diagonal arrows pointing outward.
        capsule(pen, 31, 31, 48, 14, 3.4)
        capsule(pen, 48, 14, 48, 23, 3.4)
        capsule(pen, 48, 14, 39, 14, 3.4)
        capsule(pen, 31, 31, 14, 48, 3.4)
        capsule(pen, 14, 48, 14, 39, 3.4)
        capsule(pen, 14, 48, 23, 48, 3.4)

    elif gid == "video":
        # Frame with a play triangle inside.
        ring_rr(pen, 7, 12, 48, 38, 5)
        poly_round(pen, [(26.5, 21.5), (44, 31), (26.5, 40.5)], 3.2)

    elif gid == "clock":
        # Dial with hour and minute hand.
        ring_circle(pen, 31, 31, 20, 3.4)
        capsule(pen, 31, 31, 31, 18.5, 3.2)
        capsule(pen, 31, 31, 41.5, 36.5, 3.2)

    elif gid == "keypress":
        # Keycap with a finger arrow pressing down onto it.
        capsule(pen, 31, 7, 31, 19.5, 3.2)
        capsule(pen, 31, 21, 25.5, 14.5, 3.2)
        capsule(pen, 31, 21, 36.5, 14.5, 3.2)
        ring_rr(pen, 14, 26, 34, 25, 6)

    elif gid == "play":
        # Solid play triangle with softly rounded corners.
        poly_round(pen, [(20, 12), (52, 31), (20, 50)], 5.0)

    elif gid == "pausemedia":
        # Two solid pause bars.
        rr(pen, 17, 13, 9, 36, 3.5)
        rr(pen, 36, 13, 9, 36, 3.5)

    elif gid == "netup":
        for y in (13, 31, 49):
            capsule(pen, 9, y, 35, y, 3.6)
        capsule(pen, 36.5, 13, 36.5, 49, 3.2)
        capsule(pen, 52, 12.25, 52, 52.25)
        capsule(pen, 52, 9.75, 45.5, 18.25)
        capsule(pen, 52, 9.75, 58.5, 18.25)

    elif gid == "netdown":
        for y in (13, 31, 49):
            capsule(pen, 9, y, 35, y, 3.6)
        capsule(pen, 36.5, 13, 36.5, 49, 3.2)
        capsule(pen, 52, 9.75, 52, 49.75)
        capsule(pen, 52, 52.25, 45.5, 44)
        capsule(pen, 52, 52.25, 58.5, 44)


def draw_frame_svg(pen, W):
    rr(pen, 0, 0, W, BOX_H, RADIUS_OUT)
    inner = ReverseContourPen(pen)
    rr(inner, STROKE, STROKE, W - 2 * STROKE, BOX_H - 2 * STROKE, RADIUS_IN)


def draw_label_svg(pen, d):
    if d["kind"] == "arrow":
        pts = arrow_points(d["direction"], d["W"], BOX_H)
        pen.moveTo(pts[0])
        for p in pts[1:]:
            pen.lineTo(p)
        pen.closePath()
    else:
        f = FACES[d["face"]]
        scale = FONT_SIZE / f["upem"]
        x = (d["W"] - d["tw"]) / 2
        for c in d["label"]:
            gn = f["cmap"][ord(c)]
            f["glyphs"][gn].draw(
                TransformPen(pen, (scale, 0, 0, -scale, x, d["baseline"]))
            )
            x += f["hmtx"][gn][0] * scale


def path_pair(gid):
    d = design_for(gid)
    if d["kind"] == "icon":
        ip = SVGPathPen(GLYPHS, ntos=lambda v: f"{v:.3f}")
        draw_icon_svg(ip, gid)
        return d, "", ip.getCommands()

    fp = SVGPathPen(GLYPHS, ntos=lambda v: f"{v:.3f}")
    draw_frame_svg(fp, d["W"])
    lp = SVGPathPen(GLYPHS, ntos=lambda v: f"{v:.3f}")
    draw_label_svg(lp, d)
    return d, fp.getCommands(), lp.getCommands()


PATHS = {gid: path_pair(gid) for gid, *_ in ALL_GLYPHS}
