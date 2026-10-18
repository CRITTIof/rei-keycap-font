import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pydeps"))

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

import geometry as G
from data import UNIQUE

DIST = G.OUT
DIST.mkdir(parents=True, exist_ok=True)
TTF_PATH = DIST / "KeycapTight-Regular.ttf"
WOFF2_PATH = DIST / "KeycapTight-Regular.woff2"

S = G.FONT_SCALE  # 1000 / 62
SIDE = G.SIDE_BEARING


def rr_font(pen, x, y, w, h, r):
    """Rounded rectangle in font units (y-up). Winding is irrelevant as long
    as the inner contour is reversed."""
    G.rr(pen, x, y, w, h, r)


def text_bounds_font(label, scale):
    pen = BoundsPen(G.GLYPHS)
    x = 0.0
    for c in label:
        gn = G.CMAP[ord(c)]
        G.GLYPHS[gn].draw(TransformPen(pen, (scale, 0, 0, scale, x, 0)))
        x += G.HMTX[gn][0] * scale
    return pen.bounds


def draw_key(gid):
    d = G.PATHS[gid][0]
    W = d["W"] * S
    advance = round(2 * SIDE + W)
    box_w = advance - 2 * SIDE

    ttpen = TTGlyphPen(None)
    pen = Cu2QuPen(ttpen, max_err=0.4)

    # Frame: outer and reversed inner contour.
    rr_font(pen, SIDE, 0, box_w, 1000, G.RADIUS_OUT * S)
    inner = ReverseContourPen(pen)
    rr_font(inner, SIDE + G.STROKE * S, G.STROKE * S,
            box_w - 2 * G.STROKE * S, 1000 - 2 * G.STROKE * S,
            G.RADIUS_IN * S)

    if d["kind"] == "arrow":
        pts_design = G.arrow_points(d["direction"], d["W"], G.BOX_H)
        pts = [(SIDE + x * S, (G.BOX_H - y) * S) for x, y in pts_design]
        pen.moveTo(pts[0])
        for p in pts[1:]:
            pen.lineTo(p)
        pen.closePath()
    else:
        scale = G.FONT_SIZE * S / G.UPEM
        tw = d["tw"] * S
        x = SIDE + (box_w - tw) / 2
        b = text_bounds_font(d["label"], scale)
        ymin, ymax = b[1], b[3]
        baseline = 500 - (ymin + ymax) / 2
        for c in d["label"]:
            gn = G.CMAP[ord(c)]
            G.GLYPHS[gn].draw(TransformPen(pen, (scale, 0, 0, scale, x, baseline)))
            x += G.HMTX[gn][0] * scale

    return ttpen.glyph(), advance, box_w


glyph_order = [".notdef"] + [gid for gid, *_ in UNIQUE]
glyphs = {".notdef": TTGlyphPen(None).glyph()}
hmtx = {".notdef": (500, 0)}
for gid, *_ in UNIQUE:
    glyph, advance, box_w = draw_key(gid)
    glyphs[gid] = glyph
    hmtx[gid] = (advance, SIDE)

cmap = {G.META[gid]["pua"]: gid for gid, *_ in UNIQUE}

fb = FontBuilder(1000, isTTF=True)
fb.setupGlyphOrder(glyph_order)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(hmtx)
fb.setupHorizontalHeader(ascent=1000, descent=0)
fb.setupNameTable({
    "copyright": "Copyright 2026 Keycap Tight. Glyph outlines derived from Noto Sans SemiBold, Copyright 2018 The Noto Project Authors (SIL Open Font License 1.1).",
    "familyName": "Keycap Tight",
    "styleName": "Regular",
    "uniqueFontIdentifier": "KeycapTight-Regular-1.000",
    "fullName": "Keycap Tight Regular",
    "version": "Version 1.000",
    "psName": "KeycapTight-Regular",
    "manufacturer": "Keycap Tight",
    "description": "83 content-fitted, transparent keycap glyphs with Windows primary legends. Upem 1000; glyph height equals 1em.",
    "licenseDescription": "SIL Open Font License 1.1. Includes outlines derived from Noto Sans SemiBold. See OFL.txt.",
    "licenseInfoURL": "https://openfontlicense.org/",
})
fb.setupOS2(
    sTypoAscender=1000,
    sTypoDescender=0,
    sTypoLineGap=0,
    usWinAscent=1000,
    usWinDescent=0,
    sxHeight=500,
    sCapHeight=700,
    usWeightClass=400,
    usWidthClass=5,
    fsType=0,
    achVendID="DSH ",
)
fb.setupPost()
fb.setupMaxp()
fb.save(TTF_PATH)

font = TTFont(TTF_PATH)
font.flavor = "woff2"
font.save(WOFF2_PATH)

print("saved", TTF_PATH, TTF_PATH.stat().st_size)
print("saved", WOFF2_PATH, WOFF2_PATH.stat().st_size)
print("glyphs", len(glyph_order), "cmap", len(cmap))

# Quick raster proof: all 83 glyphs on light and dark backgrounds.
labels = [gid for gid, *_ in UNIQUE]
font_px = 62
pil_font = ImageFont.truetype(str(TTF_PATH), font_px)
pad = 18
cell_w, cell_h = 210, 92
cols = 8
rows = (len(labels) + cols - 1) // cols
for mode, bg, fg in [("light", "#F7F5F0", "#20242A"), ("dark", "#1B1E24", "#F4F1EA")]:
    im = Image.new("RGB", (cols * cell_w + pad, rows * cell_h + pad), bg)
    dr = ImageDraw.Draw(im)
    for i, gid in enumerate(labels):
        cp = G.META[gid]["pua"]
        ch = chr(cp)
        bbox = dr.textbbox((0, 0), ch, font=pil_font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = pad + (i % cols) * cell_w + (cell_w - 12 - tw) // 2
        y = pad + (i // cols) * cell_h + (cell_h - 12 - th) // 2
        dr.text((x, y), ch, font=pil_font, fill=fg)
    im.save(DIST / f"font-proof-{mode}.png")
    print("proof", mode, im.size)
