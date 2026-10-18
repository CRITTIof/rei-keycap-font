import csv
import json
from pathlib import Path

import geometry as G
from data import UNIQUE, PHYS

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
        "label": label,
        "full": full,
        "glyph": gid,
        "pua": f"U+{meta['pua']:04X}",
        "codepoint": meta["pua"],
        "width": round(G.PATHS[gid][0]["W"], 3),
        "section": section,
        "folder": G.folder_name(gid),
        "svg": f"字符/{G.folder_name(gid)}/keycap.svg",
        "shared_with": others,
    })

glyphs = []
for gid, label, full, group in UNIQUE:
    meta = G.META[gid]
    glyphs.append({
        "id": gid,
        "label": label,
        "full": full,
        "group": group,
        "pua": f"U+{meta['pua']:04X}",
        "codepoint": meta["pua"],
        "width": round(G.PATHS[gid][0]["W"], 3),
        "keycodes": shared[gid],
        "folder": G.folder_name(gid),
        "svg": f"字符/{G.folder_name(gid)}/keycap.svg",
        "preview": f"字符/{G.folder_name(gid)}/preview.png",
    })

data = {
    "name": "Keycap Tight",
    "version": "1.0.0",
    "description": "83 unique, content-fitted, transparent keycap glyphs for Windows primary legends. 101 physical keycodes are mapped to these glyphs.",
    "design": {
        "box_height": 62,
        "stroke": 4,
        "radius_outer": 16,
        "radius_inner": 12,
        "padding_x": 20,
        "text_size": 42,
        "text_face": "Noto Sans SemiBold",
        "fill": "none (outline only)",
        "width_rule": "text advance width + 40",
        "height_rule": "uniform 62; glyphs vertically centered on ink",
    },
    "font": {
        "family": "Keycap Tight",
        "style": "Regular",
        "file_ttf": "KeycapTight-Regular.ttf",
        "file_woff2": "KeycapTight-Regular.woff2",
        "units_per_em": 1000,
        "glyph_height_em": 1.0,
        "pua_range": "U+E000–U+E052",
        "usage": "font-size equals the desired visual key height; line-height 1; transparent interior; single color via CSS color/currentColor.",
    },
    "stats": {
        "physical_keys": len(PHYS),
        "unique_glyphs": len(UNIQUE),
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
    ],
    "glyphs": glyphs,
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
    w.writerow(["id", "label", "full", "group", "pua", "codepoint", "width", "keycodes"])
    for g in glyphs:
        w.writerow([g["id"], g["label"], g["full"], g["group"], g["pua"], g["codepoint"], g["width"], " ".join(g["keycodes"])])

print("mapping", len(keys), "keys", len(glyphs), "glyphs")
print(json.dumps(data["stats"], ensure_ascii=False))
