import csv
import json
from pathlib import Path

import geometry as G
from data import UNIQUE, PHYS, ICONS

DIST = G.OUT
DIST.mkdir(parents=True, exist_ok=True)
SECTIONS = [
    ("function", "Function & navigation"),
    ("numbers", "Number row"),
    ("letters", "Tabs, letters & punctuation"),
    ("caps", "Caps row & modifiers"),
    ("shift", "Shift row"),
    ("mods", "Modifiers & arrows"),
    ("numpad", "Numpad"),
]

shared = {}
for code, label, gid, full, section in PHYS:
    shared.setdefault(gid, []).append(code)

keys = []
for code, label, gid, full, section in PHYS:
    meta = G.META[gid]
    others = [c for c in shared[gid] if c != code]
    keys.append({
        "code": code,
        "type": "keycap",
        "label": label,
        "full": full,
        "glyph": gid,
        "pua": f"U+{meta['pua']:04X}",
        "codepoint": meta["pua"],
        "width": round(G.PATHS[gid][0]["W"], 3),
        "section": section,
        "folder": G.folder_name(gid),
        "svg": f"glyphs/{G.folder_name(gid)}/keycap.svg",
        "shared_with": others,
    })

glyphs = []
for gid, label, full, group in UNIQUE:
    meta = G.META[gid]
    glyphs.append({
        "id": gid,
        "type": "keycap",
        "label": label,
        "full": full,
        "group": group,
        "pua": f"U+{meta['pua']:04X}",
        "codepoint": meta["pua"],
        "width": round(G.PATHS[gid][0]["W"], 3),
        "keycodes": shared[gid],
        "text": G.TEXT_CHARS.get(gid, []),
        "text_codepoints": [ord(c) for c in G.TEXT_CHARS.get(gid, [])],
        "folder": G.folder_name(gid),
        "svg": f"glyphs/{G.folder_name(gid)}/keycap.svg",
        "preview": f"glyphs/{G.folder_name(gid)}/preview.png",
    })

icons = []
for gid, label, full, group in ICONS:
    meta = G.META[gid]
    icons.append({
        "id": gid,
        "type": "icon",
        "category": group,
        "label": label,
        "full": full,
        "group": group,
        "pua": f"U+{meta['pua']:04X}",
        "codepoint": meta["pua"],
        "width": round(G.PATHS[gid][0]["W"], 3),
        "folder": G.folder_name(gid),
        "svg": f"glyphs/{G.folder_name(gid)}/icon.svg",
        "preview": f"glyphs/{G.folder_name(gid)}/preview.png",
        "style": "transparent line icon; no border, no text",
    })

software_icons = [i for i in icons if i["group"] == "software"]
hardware_icons = [i for i in icons if i["group"] == "hardware"]

text_map = []
for cp, gid in sorted(G.TEXT_CMAP.items()):
    meta = G.META[gid]
    text_map.append({
        "char": chr(cp),
        "codepoint": cp,
        "glyph": gid,
        "pua": f"U+{meta['pua']:04X}",
    })

data = {
    "name": "Keycap Tight",
    "version": "1.4.0",
    "description": "83 content-fitted keycap glyphs, 12 transparent system line icons (4 software, 8 hardware), and normal-text aliases A-Z/a-z/0-9. Letters and digits use a monospaced face. 101 physical keycodes map to the keycap glyphs.",
    "design": {
        "box_height": 62,
        "stroke": 4,
        "radius_outer": 16,
        "radius_inner": 12,
        "padding_x": 20,
        "text_size": 42,
        "text_face": "Noto Sans SemiBold",
        "letter_digit_face": "JetBrains Mono SemiBold",
        "fill": "none (outline only)",
        "width_rule": "text advance width + 40; all single letters and digits share one 65.2-unit width",
        "height_rule": "all glyphs use one 62-unit slot; keycap frames are exactly 62 tall and icons stay inside the same 62 box",
        "icon_box": "62 x 62 design units; line icons use the same 1em height",
    },
    "font": {
        "family": "Keycap Tight",
        "style": "Regular",
        "file_ttf": "KeycapTight-Regular.ttf",
        "file_woff2": "KeycapTight-Regular.woff2",
        "units_per_em": 1000,
        "glyph_height_em": 1.0,
        "pua_range": "U+E000–U+E05E",
        "text_aliases": "ASCII A-Z, a-z and 0-9 map to the matching keycap glyphs. Lowercase and uppercase share the uppercase keycap.",
        "usage": "font-size equals the desired visual key height; line-height 1; transparent interior; single color via CSS color/currentColor.",
    },
    "stats": {
        "physical_keys": len(PHYS),
        "unique_glyphs": len(UNIQUE),
        "icon_glyphs": len(ICONS),
        "software_icons": len(software_icons),
        "hardware_icons": len(hardware_icons),
        "text_aliases": len(G.TEXT_CMAP),
        "total_glyphs": len(UNIQUE) + len(ICONS),
        "duplicate_instances": len(PHYS) - len(UNIQUE),
        "sections": len(SECTIONS),
    },
    "notes": [
        "Windows primary legends only: shifted symbols and numpad navigation sublabels are intentionally omitted.",
        "Numpad digits, Enter, /, -, and . share glyphs with their main-keyboard equivalents.",
        "Left/right Shift, Ctrl, Alt and Fn share one glyph each.",
        "Clear is rendered as Num (Num Lock) for Windows.",
        "The Windows key uses event.code MetaLeft in browsers.",
        "Fn generally does not emit a browser KeyboardEvent; FnLeft/FnRight are custom mapping names.",
        "The twelve system icons are pictograms, not text, and have no keycode entry. They are split into software_icons (4) and hardware_icons (8), and share the same transparent 1em outline style.",
        "The glyph labelled ROM follows the keyboard's terminology but is drawn as a hard drive (HDD), not a ROM chip.",
        "ASCII A-Z, a-z and 0-9 are aliases for the matching keycap glyphs; for ordinary prose use a normal text font.",
        "All letter and digit keycaps use JetBrains Mono SemiBold, so Q, I, W, M and every digit have the same width.",
        "CLI and Web use a plain title bar without window dots; Web shows two horizontal content lines.",
        "App is one rounded tile with a large lower-right APP label; the border is opened behind the label so text and frame never overlap.",
        "USB is a front-view USB-A drive: the body is slightly wider than the plug, shorter than before, and open at the bottom, with no closing line.",
        "Vol uses two round-capped arcs on the right instead of chevrons.",
        "ROM keeps the hard-drive platter and actuator arm but has no bottom contact pins.",
        "GPU is narrower and keeps three bottom pins at the original spacing and line width; the fan is one slightly narrow ring.",
        "RAM is simplified to three internal rectangles and five bottom pins.",
        "Every glyph uses one 1000-unit em slot: all 83 keycap frames are exactly 1000 units tall, all 12 icons stay inside 0..1000, and every standalone SVG is 62 units high.",
    ],
    "glyphs": glyphs,
    "icons": icons,
    "software_icons": software_icons,
    "hardware_icons": hardware_icons,
    "text_map": text_map,
    "keys": keys,
}
(DIST / "keycap-tight-mapping.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

with (DIST / "keycap-tight-keymap.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["code", "label", "full", "glyph", "pua", "codepoint", "section", "width", "shared_with"])
    for k in keys:
        w.writerow([k["code"], k["label"], k["full"], k["glyph"], k["pua"], k["codepoint"], k["section"], k["width"], " ".join(k["shared_with"])])

with (DIST / "keycap-tight-glyphs.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "label", "full", "group", "pua", "codepoint", "width", "text", "text_codepoints", "keycodes"])
    for g in glyphs:
        w.writerow([g["id"], g["label"], g["full"], g["group"], g["pua"], g["codepoint"],
                    g["width"], " ".join(g["text"]), " ".join(str(c) for c in g["text_codepoints"]),
                    " ".join(g["keycodes"])])

with (DIST / "keycap-tight-icons.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "category", "label", "full", "pua", "codepoint", "width", "folder"])
    for icon in icons:
        w.writerow([icon["id"], icon["category"], icon["label"], icon["full"], icon["pua"],
                    icon["codepoint"], icon["width"], icon["folder"]])

for name, subset in (("software", software_icons), ("hardware", hardware_icons)):
    with (DIST / f"keycap-tight-{name}-icons.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "category", "label", "full", "pua", "codepoint", "width", "folder"])
        for icon in subset:
            w.writerow([icon["id"], icon["category"], icon["label"], icon["full"], icon["pua"],
                        icon["codepoint"], icon["width"], icon["folder"]])

with (DIST / "keycap-tight-text-map.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["char", "codepoint", "glyph", "pua"])
    for item in text_map:
        w.writerow([item["char"], item["codepoint"], item["glyph"], item["pua"]])

print("mapping", len(keys), "keys", len(glyphs), "keycap glyphs",
      len(icons), "icons", len(text_map), "text aliases")
print(json.dumps(data["stats"], ensure_ascii=False))
