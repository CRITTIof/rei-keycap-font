"""Shared geometry for the tight keycaps.

Design coordinates: x grows right, y grows down.  The key box is 62 px tall.
The font maps this to 1000 units/em with the box filling the em.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # KeycapTight/工作文件
OUT = ROOT.parent / "成品"                           # KeycapTight/成品
CHARS = OUT / "字符"                                 # KeycapTight/成品/字符
sys.path.insert(0, str(ROOT / "pydeps"))

from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen

from data import UNIQUE, PHYS, ICONS, ALL_GLYPHS

FONT_SRC = ROOT / "assets" / "noto-sans-semibold.ttf"
SRC = TTFont(FONT_SRC)
GLYPHS = SRC.getGlyphSet()
CMAP = SRC.getBestCmap()
HMTX = SRC["hmtx"]
UPEM = SRC["head"].unitsPerEm

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

PUA = {gid: 0xE000 + i for i, (gid, *_rest) in enumerate(ALL_GLYPHS)}
META = {}
for gid, label, full, group in UNIQUE:
    META[gid] = {"label": label, "full": full, "group": group,
                 "pua": PUA[gid], "kind": "keycap"}
for gid, label, full, group in ICONS:
    META[gid] = {"label": label, "full": full, "group": group,
                 "pua": PUA[gid], "kind": "icon"}

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


def text_width(label):
    return sum(HMTX[CMAP[ord(c)]][0] * SCALE for c in label)


def text_bounds(label):
    pen = BoundsPen(GLYPHS)
    x = 0.0
    for c in label:
        gn = CMAP[ord(c)]
        GLYPHS[gn].draw(TransformPen(pen, (SCALE, 0, 0, SCALE, x, 0)))
        x += HMTX[gn][0] * SCALE
    return pen.bounds


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
    tw = text_width(label)
    W = tw + 2 * PAD_X
    b = text_bounds(label)
    ymin, ymax = b[1], b[3]
    baseline = BOX_H / 2 + (ymin + ymax) / 2
    return {"W": W, "tw": tw, "baseline": baseline, "kind": "text", "label": label}


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


def ring_rr(pen, x, y, w, h, r, stroke=ICON_STROKE):
    s = stroke
    rr(pen, x - s / 2, y - s / 2, w + s, h + s, r + s / 2)
    inner = ReverseContourPen(pen)
    rr(inner, x + s / 2, y + s / 2, w - s, h - s, max(0.1, r - s / 2))


def ring_circle(pen, cx, cy, r, stroke=ICON_STROKE):
    s = stroke
    circle(pen, cx, cy, r + s / 2)
    circle(ReverseContourPen(pen), cx, cy, max(0.1, r - s / 2))


def draw_icon_svg(pen, gid):
    """Filled line-art outlines for the six system pictograms.

    All coordinates live in a 62 x 62 design box.  The shapes are built from
    capsules, rings and dots so the same path can be used by SVG and by the
    font (fonts can only fill, not stroke).
    """
    if gid == "cpu":
        ring_rr(pen, 13, 13, 36, 36, 5)
        ring_rr(pen, 25, 25, 12, 12, 2)
        for p in (22, 31, 40):
            capsule(pen, p, 8, p, 14)
            capsule(pen, p, 48, p, 54)
            capsule(pen, 8, p, 14, p)
            capsule(pen, 48, p, 54, p)

    elif gid == "gpu":
        # The bracket is deliberately separated from the card body.
        ring_rr(pen, 14, 20, 38, 20, 3)
        capsule(pen, 6, 17, 6, 45)
        capsule(pen, 3.5, 20, 7, 20)
        capsule(pen, 3.5, 42, 7, 42)
        ring_circle(pen, 34, 30, 6.5, 3.2)
        circle(pen, 34, 30, 1.6)
        for deg in (90, 210, 330):
            a = math.radians(deg)
            capsule(pen, 34, 30, 34 + 4.8 * math.cos(a), 30 + 4.8 * math.sin(a), 2.4)
        for x in (20, 28, 36, 44):
            capsule(pen, x, 40, x, 45, 2.2)

    elif gid == "ram":
        ring_rr(pen, 6, 23, 50, 15, 3)
        for x in (13, 23, 33, 43):
            ring_rr(pen, x, 27, 6, 6, 1.2, 2.2)
        for x in (9, 16, 23, 30, 37, 44, 51):
            capsule(pen, x, 38, x, 43, 2.2)

    elif gid == "rom":
        # "ROM" in this keyboard means the hard drive: enclosure, platter,
        # spindle, actuator arm and SATA-side contacts.
        ring_rr(pen, 10, 17, 42, 28, 3)
        ring_circle(pen, 25, 31, 8.0, 3.2)
        circle(pen, 25, 31, 2.0)
        circle(pen, 45, 21, 2.2)
        capsule(pen, 45, 21, 30, 30, 3.0)
        for x in (38, 43, 48):
            capsule(pen, x, 45, x, 49, 2.2)

    elif gid == "netup":
        for y in (20, 31, 42):
            capsule(pen, 9, y, 35, y, 3.2)
        capsule(pen, 36, 20, 36, 42, 3.2)
        capsule(pen, 50, 46, 50, 20)
        capsule(pen, 50, 15, 43, 23)
        capsule(pen, 50, 15, 57, 23)

    elif gid == "netdown":
        for y in (20, 31, 42):
            capsule(pen, 9, y, 35, y, 3.2)
        capsule(pen, 36, 20, 36, 42, 3.2)
        capsule(pen, 50, 16, 50, 42)
        capsule(pen, 50, 47, 43, 39)
        capsule(pen, 50, 47, 57, 39)


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
        x = (d["W"] - d["tw"]) / 2
        for c in d["label"]:
            gn = CMAP[ord(c)]
            GLYPHS[gn].draw(TransformPen(pen, (SCALE, 0, 0, -SCALE, x, d["baseline"])))
            x += HMTX[gn][0] * SCALE


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
