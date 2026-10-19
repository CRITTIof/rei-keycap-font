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
from data import PHYS, UNIQUE, ICONS, ALL_GLYPHS
from fontTools.ttLib import TTFont

OUT = G.OUT
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


mapping = json.loads((OUT / "keycap-tight-mapping.json").read_text(encoding="utf-8"))
glyphs = mapping["glyphs"]
icons = mapping["icons"]
keys = mapping["keys"]
check(len(glyphs) == 83, f"mapping glyphs = {len(glyphs)}")
check(len(icons) == 6, f"mapping icons = {len(icons)}")
check(len(keys) == 101, f"mapping keys = {len(keys)}")
check(len({k["code"] for k in keys}) == 101, "duplicate event.code")
check(len({g["folder"] for g in glyphs + icons}) == 89, "duplicate glyph folder")

for g in glyphs + icons:
    folder = OUT / "字符" / g["folder"]
    check(folder.is_dir(), f"missing folder {folder}")
    check((folder / "glyph.json").is_file(), f"missing glyph.json {folder}")
    check((folder / "preview.png").is_file(), f"missing preview {folder}")
    check((folder / Path(g["svg"]).name).is_file(), f"missing svg {folder}")
    meta = json.loads((folder / "glyph.json").read_text(encoding="utf-8"))
    check(meta["codepoint"] == g["codepoint"], f"codepoint mismatch {folder}")

check(len(list((OUT / "字符").glob("U+*/*.svg"))) == 89, "glyph SVG count")
check(len(list((OUT / "字符").glob("U+*/preview.png"))) == 89, "glyph preview count")

sprite = (OUT / "keycap-tight-sprite.svg").read_text(encoding="utf-8")
check(sprite.count("<symbol id=") == 89, "sprite symbols")

specimen = (OUT / "keycap-tight-specimen.svg").read_text(encoding="utf-8")
check(specimen.count('data-glyph="') == 89, "specimen glyph count")

demo = (OUT / "demo.html").read_text(encoding="utf-8")
check(demo.count('class="cap"') == 83, "demo keycap buttons")
check("KeycapTight-Regular.woff2" in demo, "demo font URL")

font = TTFont(OUT / "KeycapTight-Regular.ttf")
cmap = font.getBestCmap()
check(len(cmap) == 89, f"font cmap = {len(cmap)}")
check(set(cmap) == set(range(0xE000, 0xE000 + 89)), "font PUA range")
check(font["head"].unitsPerEm == 1000, "font UPEM")
check(font["hhea"].ascent == 1000 and font["hhea"].descent == 0, "font vertical metrics")
check((OUT / "KeycapTight-Regular.woff2").read_bytes()[:4] == b"wOF2", "woff2 signature")
check((OUT / "keycap-tight-icons.svg").is_file(), "icon sheet SVG")
check((OUT / "keycap-tight-icons.png").is_file(), "icon sheet PNG")

zip_path = OUT / "KeycapTight-Windows.zip"
expected_files = sum(
    1 for p in OUT.rglob("*")
    if p.is_file() and p != zip_path and "__pycache__" not in p.parts
)
with zipfile.ZipFile(zip_path) as zf:
    names = zf.namelist()
    check(len(names) == expected_files, f"zip entries = {len(names)} / {expected_files}")
    for required in ["README.md", "OFL.txt", "demo.html", "demo-preview.png",
                     "KeycapTight-Regular.woff2", "字符/index.csv",
                     "keycap-tight-icons.csv", "keycap-tight-icons.svg",
                     "keycap-tight-icons.png"]:
        check(required in names, f"zip missing {required}")
    check(sum(n.startswith("字符/U+") and n.endswith(".svg") for n in names) == 89,
          "zip glyph svg count")

if errors:
    print("INVALID")
    for err in errors:
        print(" -", err)
    raise SystemExit(1)

print("ALL VALID")
print(f"101 physical keys -> 83 keycaps + 6 icons, 89 glyph folders, {len(names)} zip files")
print(f"font: {len(cmap)} PUA glyphs, {font['head'].unitsPerEm} upem")
