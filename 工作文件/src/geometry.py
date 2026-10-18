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

from data import UNIQUE, PHYS

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

PUA = {gid: 0xE000 + i for i, (gid, *_rest) in enumerate(UNIQUE)}
META = {
    gid: {"label": label, "full": full, "group": group, "pua": PUA[gid]}
    for gid, label, full, group in UNIQUE
}

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
    fp = SVGPathPen(GLYPHS, ntos=lambda v: f"{v:.3f}")
    draw_frame_svg(fp, d["W"])
    lp = SVGPathPen(GLYPHS, ntos=lambda v: f"{v:.3f}")
    draw_label_svg(lp, d)
    return d, fp.getCommands(), lp.getCommands()


PATHS = {gid: path_pair(gid) for gid, *_ in UNIQUE}
