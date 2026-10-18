"""Sanity-check the generated 成品 tree and ZIP."""
import json
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))
sys.path.insert(0, str(HERE / "pydeps"))

import geometry as G
from data import PHYS, UNIQUE
from fontTools.ttLib import TTFont

OUT = G.OUT
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


mapping = json.loads((OUT / "keycap-tight-mapping.json").read_text(encoding="utf-8"))
glyphs = mapping["glyphs"]
keys = mapping["keys"]
check(len(glyphs) == 83, f"mapping glyphs = {len(glyphs)}")
check(len(keys) == 101, f"mapping keys = {len(keys)}")
check(len({k["code"] for k in keys}) == 101, "duplicate event.code")
check(len({g["folder"] for g in glyphs}) == 83, "duplicate glyph folder")

for g in glyphs:
    folder = OUT / "字符" / g["folder"]
    check(folder.is_dir(), f"missing folder {folder}")
    check((folder / "keycap.svg").is_file(), f"missing svg {folder}")
    check((folder / "glyph.json").is_file(), f"missing glyph.json {folder}")
    check((folder / "preview.png").is_file(), f"missing preview {folder}")
    meta = json.loads((folder / "glyph.json").read_text(encoding="utf-8"))
    check(meta["codepoint"] == g["codepoint"], f"codepoint mismatch {folder}")

check(len(list((OUT / "字符").glob("U+*/keycap.svg"))) == 83, "character SVG count")
check(len(list((OUT / "字符").glob("U+*/preview.png"))) == 83, "character preview count")

sprite = (OUT / "keycap-tight-sprite.svg").read_text(encoding="utf-8")
check(sprite.count("<symbol id=") == 83, "sprite symbols")

specimen = (OUT / "keycap-tight-specimen.svg").read_text(encoding="utf-8")
check(specimen.count('data-glyph="') == 83, "specimen glyph count")

demo = (OUT / "demo.html").read_text(encoding="utf-8")
check(demo.count('class="cap"') == 83, "demo keycap buttons")
check("KeycapTight-Regular.woff2" in demo, "demo font URL")

font = TTFont(OUT / "KeycapTight-Regular.ttf")
cmap = font.getBestCmap()
check(len(cmap) == 83, f"font cmap = {len(cmap)}")
check(set(cmap) == set(range(0xE000, 0xE000 + 83)), "font PUA range")
check(font["head"].unitsPerEm == 1000, "font UPEM")
check(font["hhea"].ascent == 1000 and font["hhea"].descent == 0, "font vertical metrics")
check((OUT / "KeycapTight-Regular.woff2").read_bytes()[:4] == b"wOF2", "woff2 signature")

zip_path = OUT / "KeycapTight-Windows.zip"
with zipfile.ZipFile(zip_path) as zf:
    names = zf.namelist()
    check(len(names) == 265, f"zip entries = {len(names)}")
    for required in ["README.md", "OFL.txt", "demo.html", "demo-preview.png",
                     "KeycapTight-Regular.woff2", "字符/index.csv"]:
        check(required in names, f"zip missing {required}")
    check(sum(n.startswith("字符/U+") and n.endswith("/keycap.svg") for n in names) == 83,
          "zip character svg count")

if errors:
    print("INVALID")
    for err in errors:
        print(" -", err)
    raise SystemExit(1)

print("ALL VALID")
print(f"101 physical keys -> 83 unique glyphs, 83 character folders, {len(names)} zip files")
print(f"font: {len(cmap)} PUA glyphs, {font['head'].unitsPerEm} upem")
