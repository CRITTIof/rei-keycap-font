import csv
import json
from pathlib import Path
from xml.sax.saxutils import escape as xesc

import geometry as G
from data import UNIQUE, PHYS

DIST = G.OUT
DIST.mkdir(parents=True, exist_ok=True)
G.CHARS.mkdir(parents=True, exist_ok=True)

# Physical keycodes sharing each glyph, used in the per-character metadata.
SHARED = {}
for code, _label, gid, _full, _section in PHYS:
    SHARED.setdefault(gid, []).append(code)

INK = "#20242A"
PAPER = "#F7F5F0"
MUTED = "#77736B"
HAIR = "#D8D2C7"


def symbol_svg(gid):
    meta = G.META[gid]
    d, frame, label = G.PATHS[gid]
    return f'''  <symbol id="key-{gid}" viewBox="0 0 {d['W']:.3f} 62" data-glyph="{gid}" data-label="{xesc(meta['label'])}" data-full="{xesc(meta['full'])}" data-pua="U+{meta['pua']:04X}">
    <title>{xesc(meta['label'])} — {xesc(meta['full'])}</title>
    <g fill="currentColor">
      <path class="keycap-frame" d="{frame}"/>
      <path class="keycap-label" d="{label}"/>
    </g>
  </symbol>'''


sprite = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute;overflow:hidden" aria-hidden="true">
  <!-- Keycap Tight — 83 unique primary-only keycaps, Windows legends.
       ViewBox height is 62. Use with <svg viewBox="0 0 W 62"><use href="#key-..."/></svg>.
       Both path classes inherit currentColor; override .keycap-frame / .keycap-label to theme separately. -->
  <defs>
{chr(10).join(symbol_svg(gid) for gid, *_ in UNIQUE)}
  </defs>
</svg>
'''
(DIST / "keycap-tight-sprite.svg").write_text(sprite, encoding="utf-8")

# One folder per unique character.
for gid, label, full, group in UNIQUE:
    d, frame, label_path = G.PATHS[gid]
    w = d["W"]
    meta = G.META[gid]
    folder = G.CHARS / G.folder_name(gid)
    folder.mkdir(parents=True, exist_ok=True)
    one = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}" height="62" viewBox="0 0 {w:.3f} 62" role="img" aria-label="{xesc(label)}">
  <title>{xesc(label)} — {xesc(full)}</title>
  <g fill="currentColor">
    <path class="keycap-frame" d="{frame}"/>
    <path class="keycap-label" d="{label_path}"/>
  </g>
</svg>
'''
    (folder / "keycap.svg").write_text(one, encoding="utf-8")
    glyph = {
        "id": gid,
        "label": label,
        "full": full,
        "group": group,
        "pua": f"U+{meta['pua']:04X}",
        "codepoint": meta["pua"],
        "width": round(w, 3),
        "keycodes": SHARED[gid],
        "folder": folder.name,
        "svg": "keycap.svg",
        "preview": "preview.png",
    }
    (folder / "glyph.json").write_text(
        json.dumps(glyph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

with (G.CHARS / "index.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["pua", "label", "full", "group", "width", "folder", "keycodes"])
    for gid, label, full, group in UNIQUE:
        meta = G.META[gid]
        writer.writerow([
            f"U+{meta['pua']:04X}", label, full, group,
            round(G.PATHS[gid][0]["W"], 3), G.folder_name(gid),
            " ".join(SHARED[gid]),
        ])

# Specimen layout -----------------------------------------------------------
SECTIONS = [
    ("01", "Function & navigation", ["escape", *[f"f{i}" for i in range(1, 13)], "insert", "delete", "home", "end", "pageup", "pagedown"]),
    ("02", "Number row", ["backquote", *[f"digit{i}" for i in range(1, 10)], "digit0", "minus", "equal", "backspace"]),
    ("03", "Tabs, letters & punctuation", ["tab", *[f"key{c}" for c in "qwertyuiop"], "bracketleft", "bracketright", "backslash", "capslock", *[f"key{c}" for c in "asdfghjkl"], "semicolon", "quote", "enter", "shift", *[f"key{c}" for c in "zxcvbnm"], "comma", "period", "slash"]),
    ("04", "Modifiers & arrows", ["ctrl", "fn", "win", "alt", "space", "arrowleft", "arrowup", "arrowdown", "arrowright"]),
    ("05", "Numpad-only glyphs", ["num", "asterisk", "plus"]),
]

W = 2200
MARGIN = 110
RIGHT = W - MARGIN
GAP = 22
ROW_GAP = 24
HEADER_H = 26

positions = []
y = 168
for num, title, keys in SECTIONS:
    section_y = y
    y += HEADER_H + 20
    x = MARGIN
    row_top = y
    for gid in keys:
        w = G.PATHS[gid][0]["W"]
        if x + w > RIGHT:
            x = MARGIN
            y += G.BOX_H + ROW_GAP
        positions.append((gid, x, y))
        x += w + GAP
    y += G.BOX_H + 54

H = y + 24

parts = []
for gid, x, yy in positions:
    d, frame, label = G.PATHS[gid]
    meta = G.META[gid]
    parts.append(f'''  <g transform="translate({x:.3f} {yy:.3f})" data-glyph="{gid}">
    <title>{xesc(meta['label'])} — {xesc(meta['full'])}</title>
    <path class="keycap-frame" d="{frame}" fill="{INK}"/>
    <path class="keycap-label" d="{label}" fill="{INK}"/>
  </g>''')

sections_svg = []
for num, title, keys in SECTIONS:
    y0 = min(yy for gid, x, yy in positions if gid in keys) - HEADER_H - 20
    sections_svg.append(f'''  <g class="section-head">
    <text x="{MARGIN}" y="{y0}" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="2.8" fill="{MUTED}">{num} / {xesc(title.upper())}</text>
    <text x="{RIGHT}" y="{y0}" text-anchor="end" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="2.2" fill="{MUTED}">{len(keys)}</text>
    <line x1="{MARGIN}" y1="{y0+13}" x2="{RIGHT}" y2="{y0+13}" stroke="{HAIR}" stroke-width="1"/>
  </g>''')

specimen = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{PAPER}"/>
  <text x="{MARGIN}" y="72" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="24" font-weight="600" letter-spacing="6" fill="{INK}">KEYCAP TIGHT / WINDOWS</text>
  <text x="{MARGIN}" y="104" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="13" font-weight="400" letter-spacing="1.2" fill="{MUTED}">83 UNIQUE PRIMARY-ONLY KEYS · 101 PHYSICAL KEYS · TRANSPARENT FILL · CONTENT-FITTED OUTLINE</text>
  <text x="{RIGHT}" y="72" text-anchor="end" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="2.2" fill="{MUTED}">NOTO SANS SEMIBOLD</text>
  <text x="{RIGHT}" y="104" text-anchor="end" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="2.2" fill="{MUTED}">62 / 4 / 16</text>
  <line x1="{MARGIN}" y1="128" x2="{RIGHT}" y2="128" stroke="{INK}" stroke-width="1"/>
{chr(10).join(sections_svg)}
{chr(10).join(parts)}
  <line x1="{MARGIN}" y1="{H-54}" x2="{RIGHT}" y2="{H-54}" stroke="{HAIR}" stroke-width="1"/>
  <text x="{MARGIN}" y="{H-26}" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="11" font-weight="600" letter-spacing="2" fill="{MUTED}">DUPLICATES SHARE ONE GLYPH · WINDOWS PRIMARY LEGENDS ONLY</text>
  <text x="{RIGHT}" y="{H-26}" text-anchor="end" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="11" font-weight="600" letter-spacing="2" fill="{MUTED}">83 GLYPHS / 101 KEYCODES</text>
</svg>
'''
(DIST / "keycap-tight-specimen.svg").write_text(specimen, encoding="utf-8")

print(DIST / "keycap-tight-sprite.svg", len(sprite))
print(DIST / "keycap-tight-specimen.svg", len(specimen), "height", H)
print("character folders", len(list(G.CHARS.glob("U+*"))))
