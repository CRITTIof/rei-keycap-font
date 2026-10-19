from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.ttLib import TTFont

import geometry as G
from data import ALL_GLYPHS

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


def draw_key(gid):
    d = G.PATHS[gid][0]
    W = d["W"] * S
    advance = round(2 * SIDE + W)
    box_w = advance - 2 * SIDE

    ttpen = TTGlyphPen(None)
    pen = Cu2QuPen(ttpen, max_err=0.4)

    if d["kind"] == "icon":
        # Icons are already filled outlines in a 62-unit design box.  Flip
        # y for font coordinates and center them in the em.
        icon_pen = TransformPen(pen, (S, 0, 0, -S, SIDE, 1000))
        G.draw_icon_svg(icon_pen, gid)
        return ttpen.glyph(), advance, box_w

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
        face = G.FACES[d["face"]]
        scale = G.FONT_SIZE * S / face["upem"]
        tw = d["tw"] * S
        x = SIDE + (box_w - tw) / 2
        baseline = 1000 - d["baseline"] * S
        for c in d["label"]:
            gn = face["cmap"][ord(c)]
            face["glyphs"][gn].draw(
                TransformPen(pen, (scale, 0, 0, scale, x, baseline))
            )
            x += face["hmtx"][gn][0] * scale

    return ttpen.glyph(), advance, box_w


glyph_order = [".notdef"] + [gid for gid, *_ in ALL_GLYPHS]
glyphs = {".notdef": TTGlyphPen(None).glyph()}
hmtx = {".notdef": (500, 0)}
for gid, *_ in ALL_GLYPHS:
    glyph, advance, box_w = draw_key(gid)
    glyphs[gid] = glyph
    hmtx[gid] = (advance, SIDE)

cmap = {G.META[gid]["pua"]: gid for gid, *_ in ALL_GLYPHS}
cmap.update(G.TEXT_CMAP)

fb = FontBuilder(1000, isTTF=True)
fb.setupGlyphOrder(glyph_order)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(hmtx)
fb.setupHorizontalHeader(ascent=1000, descent=0)
fb.setupNameTable({
    "copyright": "Copyright 2026 Keycap Tight. Glyph outlines derived from Noto Sans SemiBold, Copyright 2018 The Noto Project Authors, and JetBrains Mono SemiBold, Copyright 2020 The JetBrains Mono Project Authors (SIL Open Font License 1.1).",
    "familyName": "Keycap Tight",
    "styleName": "Regular",
    "uniqueFontIdentifier": "KeycapTight-Regular-1.400",
    "fullName": "Keycap Tight Regular",
    "version": "Version 1.400",
    "psName": "KeycapTight-Regular",
    "manufacturer": "Keycap Tight",
    "description": "83 content-fitted keycap glyphs with Windows primary legends, 12 transparent system line icons, and normal-text aliases for A-Z/a-z/0-9. Letters and digits use a monospaced face. Upem 1000; glyph height equals 1em.",
    "licenseDescription": "SIL Open Font License 1.1. Includes outlines derived from Noto Sans SemiBold and JetBrains Mono SemiBold. See OFL.txt and OFL-JetBrainsMono.txt.",
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
