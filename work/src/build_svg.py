import csv
import json
from pathlib import Path
from xml.sax.saxutils import escape as xesc

import geometry as G
from data import UNIQUE, PHYS, ICONS, ALL_GLYPHS

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
    d, frame, body = G.PATHS[gid]
    if meta["kind"] == "icon":
        inner = f'<path class="system-icon" d="{body}"/>'
    else:
        inner = (f'<path class="keycap-frame" d="{frame}"/>'
                 f'<path class="keycap-label" d="{body}"/>')
    return f'''  <symbol id="key-{gid}" viewBox="0 0 {d['W']:.3f} 62" data-glyph="{gid}" data-kind="{meta['kind']}" data-label="{xesc(meta['label'])}" data-full="{xesc(meta['full'])}" data-pua="U+{meta['pua']:04X}">
    <title>{xesc(meta['label'])} — {xesc(meta['full'])}</title>
    <g fill="currentColor">
      {inner}
    </g>
  </symbol>'''


sprite = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute;overflow:hidden" aria-hidden="true">
  <!-- Keycap Tight — 83 primary-only keycaps + 12 system line icons.
       ViewBox height is 62. Use with <svg viewBox="0 0 W 62"><use href="#key-..."/></svg>.
       All glyphs inherit currentColor; override .keycap-frame / .keycap-label
       or .system-icon to theme them separately. -->
  <defs>
{chr(10).join(symbol_svg(gid) for gid, *_ in ALL_GLYPHS)}
  </defs>
</svg>
'''
(DIST / "keycap-tight-sprite.svg").write_text(sprite, encoding="utf-8")

# One folder per glyph: 83 keycaps + 12 system icons.
for gid, label, full, group in ALL_GLYPHS:
    d, frame, body = G.PATHS[gid]
    w = d["W"]
    meta = G.META[gid]
    is_icon = meta["kind"] == "icon"
    svg_name = "icon.svg" if is_icon else "keycap.svg"
    folder = G.CHARS / G.folder_name(gid)
    folder.mkdir(parents=True, exist_ok=True)
    if is_icon:
        markup = f'<path class="system-icon" d="{body}"/>'
    else:
        markup = (f'<path class="keycap-frame" d="{frame}"/>\n'
                  f'    <path class="keycap-label" d="{body}"/>')
    one = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}" height="62" viewBox="0 0 {w:.3f} 62" role="img" aria-label="{xesc(label)}">
  <title>{xesc(label)} — {xesc(full)}</title>
  <g fill="currentColor">
    {markup}
  </g>
</svg>
'''
    (folder / svg_name).write_text(one, encoding="utf-8")
    glyph = {
        "id": gid,
        "type": meta["kind"],
        "label": label,
        "full": full,
        "group": group,
        "pua": f"U+{meta['pua']:04X}",
        "codepoint": meta["pua"],
        "width": round(w, 3),
        "keycodes": SHARED.get(gid, []),
        "text": G.TEXT_CHARS.get(gid, []),
        "folder": folder.name,
        "svg": svg_name,
        "preview": "preview.png",
    }
    (folder / "glyph.json").write_text(
        json.dumps(glyph, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

with (G.CHARS / "index.csv").open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["pua", "type", "label", "full", "group", "width", "folder", "text", "keycodes"])
    for gid, label, full, group in ALL_GLYPHS:
        meta = G.META[gid]
        writer.writerow([
            f"U+{meta['pua']:04X}", meta["kind"], label, full, group,
            round(G.PATHS[gid][0]["W"], 3), G.folder_name(gid),
            " ".join(G.TEXT_CHARS.get(gid, [])),
            " ".join(SHARED.get(gid, [])),
        ])

# Specimen layout -----------------------------------------------------------
SOFTWARE_IDS = [gid for gid, _label, _full, group in ICONS if group == "software"]
HARDWARE_IDS = [gid for gid, _label, _full, group in ICONS if group == "hardware"]

SECTIONS = [
    ("01", "Function & navigation", ["escape", *[f"f{i}" for i in range(1, 13)], "insert", "delete", "home", "end", "pageup", "pagedown"]),
    ("02", "Number row", ["backquote", *[f"digit{i}" for i in range(1, 10)], "digit0", "minus", "equal", "backspace"]),
    ("03", "Tabs, letters & punctuation", ["tab", *[f"key{c}" for c in "qwertyuiop"], "bracketleft", "bracketright", "backslash", "capslock", *[f"key{c}" for c in "asdfghjkl"], "semicolon", "quote", "enter", "shift", *[f"key{c}" for c in "zxcvbnm"], "comma", "period", "slash"]),
    ("04", "Modifiers & arrows", ["ctrl", "fn", "win", "alt", "space", "arrowleft", "arrowup", "arrowdown", "arrowright"]),
    ("05", "Numpad-only glyphs", ["num", "asterisk", "plus"]),
    ("06", "Software icons", SOFTWARE_IDS),
    ("07", "Hardware icons", HARDWARE_IDS),
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
    d, frame, body = G.PATHS[gid]
    meta = G.META[gid]
    if meta["kind"] == "icon":
        drawn = f'<path class="system-icon" d="{body}" fill="{INK}"/>'
    else:
        drawn = (f'<path class="keycap-frame" d="{frame}" fill="{INK}"/>'
                 f'<path class="keycap-label" d="{body}" fill="{INK}"/>')
    parts.append(f'''  <g transform="translate({x:.3f} {yy:.3f})" data-glyph="{gid}" data-kind="{meta['kind']}">
    <title>{xesc(meta['label'])} — {xesc(meta['full'])}</title>
    {drawn}
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
  <text x="{MARGIN}" y="72" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="24" font-weight="600" letter-spacing="6" fill="{INK}">KEYCAP TIGHT / WINDOWS + SYSTEM</text>
  <text x="{MARGIN}" y="104" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="13" font-weight="400" letter-spacing="1.2" fill="{MUTED}">83 KEYCAPS + 12 SYSTEM ICONS · MONO A-Z/0-9 · 101 PHYSICAL KEYS · TRANSPARENT FILL</text>
  <text x="{RIGHT}" y="72" text-anchor="end" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="2.2" fill="{MUTED}">NOTO SANS + JETBRAINS MONO</text>
  <text x="{RIGHT}" y="104" text-anchor="end" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="2.2" fill="{MUTED}">62 / 4 / 16</text>
  <line x1="{MARGIN}" y1="128" x2="{RIGHT}" y2="128" stroke="{INK}" stroke-width="1"/>
{chr(10).join(sections_svg)}
{chr(10).join(parts)}
  <line x1="{MARGIN}" y1="{H-54}" x2="{RIGHT}" y2="{H-54}" stroke="{HAIR}" stroke-width="1"/>
  <text x="{MARGIN}" y="{H-26}" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="11" font-weight="600" letter-spacing="2" fill="{MUTED}">DUPLICATES SHARE ONE GLYPH · WINDOWS PRIMARY LEGENDS ONLY</text>
  <text x="{RIGHT}" y="{H-26}" text-anchor="end" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="11" font-weight="600" letter-spacing="2" fill="{MUTED}">95 GLYPHS / 101 KEYCODES</text>
</svg>
'''
(DIST / "keycap-tight-specimen.svg").write_text(specimen, encoding="utf-8")

# System-icon overview ------------------------------------------------------
SHEET_W = 1100
CELL = 240
MARGIN = 70
ICON_SCALE = 2.0
ICON_SIZE = 62 * ICON_SCALE
sheet_parts = []
y_cursor = 40
for title, ids in (("SOFTWARE ICONS", SOFTWARE_IDS), ("HARDWARE ICONS", HARDWARE_IDS)):
    sheet_parts.append(
        f'  <text x="{MARGIN}" y="{y_cursor}" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" '
        f'font-size="11" font-weight="600" letter-spacing="2.4" fill="{MUTED}">{title} / {len(ids)}</text>'
    )
    y_icons = y_cursor + 18
    for i, gid in enumerate(ids):
        meta = G.META[gid]
        body = G.PATHS[gid][2]
        col, row = i % 4, i // 4
        x = MARGIN + col * CELL + (CELL - ICON_SIZE) / 2
        y = y_icons + row * 200
        cx = MARGIN + col * CELL + CELL / 2
        sheet_parts.append(f'''  <g transform="translate({x:.3f} {y}) scale({ICON_SCALE})">
    <path class="system-icon" d="{body}" fill="{INK}"/>
  </g>
  <text x="{cx}" y="{y + 145}" text-anchor="middle" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="1.8" fill="{INK}">{xesc(meta['label'])}</text>
  <text x="{cx}" y="{y + 164}" text-anchor="middle" font-family="Noto Sans SemiBold, Noto Sans, Segoe UI, Arial, sans-serif" font-size="10" font-weight="400" letter-spacing="1.2" fill="{MUTED}">U+{meta['pua']:04X} · {xesc(meta['full'].upper())}</text>''')
    y_cursor += 18 + ((len(ids) + 3) // 4) * 200 + 38

SHEET_H = y_cursor + 10
icon_sheet = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{SHEET_W}" height="{SHEET_H}" viewBox="0 0 {SHEET_W} {SHEET_H}">
  <rect width="{SHEET_W}" height="{SHEET_H}" fill="{PAPER}"/>
{chr(10).join(sheet_parts)}
</svg>
'''
(DIST / "keycap-tight-icons.svg").write_text(icon_sheet, encoding="utf-8")

print(DIST / "keycap-tight-sprite.svg", len(sprite))
print(DIST / "keycap-tight-specimen.svg", len(specimen), "height", H)
print(DIST / "keycap-tight-icons.svg", SHEET_W, "x", SHEET_H)
print("character folders", len(list(G.CHARS.glob("U+*"))))
