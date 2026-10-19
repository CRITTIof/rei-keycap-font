"""Sanity-check the generated dist tree and ZIP."""
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
check(mapping["version"] == "1.4.0", f"mapping version = {mapping['version']}")
glyphs = mapping["glyphs"]
icons = mapping["icons"]
software_icons = mapping["software_icons"]
hardware_icons = mapping["hardware_icons"]
text_map = mapping["text_map"]
keys = mapping["keys"]
check(len(glyphs) == 83, f"mapping glyphs = {len(glyphs)}")
check(len(icons) == 12, f"mapping icons = {len(icons)}")
check(len(software_icons) == 4, f"software icons = {len(software_icons)}")
check(len(hardware_icons) == 8, f"hardware icons = {len(hardware_icons)}")
check(len(text_map) == 62, f"text aliases = {len(text_map)}")
check(len(keys) == 101, f"mapping keys = {len(keys)}")
check(len({k["code"] for k in keys}) == 101, "duplicate event.code")
check(len({g["folder"] for g in glyphs + icons}) == 95, "duplicate glyph folder")

for g in glyphs + icons:
    folder = OUT / "glyphs" / g["folder"]
    check(folder.is_dir(), f"missing folder {folder}")
    check((folder / "glyph.json").is_file(), f"missing glyph.json {folder}")
    check((folder / "preview.png").is_file(), f"missing preview {folder}")
    check((folder / Path(g["svg"]).name).is_file(), f"missing svg {folder}")
    meta = json.loads((folder / "glyph.json").read_text(encoding="utf-8"))
    check(meta["codepoint"] == g["codepoint"], f"codepoint mismatch {folder}")

check(len(list((OUT / "glyphs").glob("U+*/*.svg"))) == 95, "glyph SVG count")
check(len(list((OUT / "glyphs").glob("U+*/preview.png"))) == 95, "glyph preview count")

sprite = (OUT / "keycap-tight-sprite.svg").read_text(encoding="utf-8")
check(sprite.count("<symbol id=") == 95, "sprite symbols")

specimen = (OUT / "keycap-tight-specimen.svg").read_text(encoding="utf-8")
check(specimen.count('data-glyph="') == 95, "specimen glyph count")

demo = (OUT / "demo.html").read_text(encoding="utf-8")
check(demo.count('class="cap"') == 83, "demo keycap buttons")
check("KeycapTight-Regular.woff2" in demo, "demo font URL")

font = TTFont(OUT / "KeycapTight-Regular.ttf")
cmap = font.getBestCmap()
check(len(cmap) == 157, f"font cmap = {len(cmap)}")
expected_cmap = set(range(0xE000, 0xE000 + 95)) | {ord(c) for c in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"}
check(set(cmap) == expected_cmap, "font PUA + ASCII range")
check(cmap[ord("A")] == cmap[ord("a")] == "keya", "A/a alias")
check(cmap[ord("0")] == "digit0", "0 alias")
check(font["head"].unitsPerEm == 1000, "font UPEM")
check(font["hhea"].ascent == 1000 and font["hhea"].descent == 0, "font vertical metrics")
glyf = font["glyf"]
keycap_heights = set()
for glyph in glyphs:
    outline = glyf[glyph["id"]]
    check(outline.yMin >= 0 and outline.yMax <= 1000,
          f"glyph outside 1em slot: {glyph['id']} {outline.yMin}..{outline.yMax}")
    if glyph["type"] == "keycap":
        keycap_heights.add(outline.yMax - outline.yMin)
for glyph in icons:
    outline = glyf[glyph["id"]]
    check(outline.yMin >= 0 and outline.yMax <= 1000,
          f"icon outside 1em slot: {glyph['id']} {outline.yMin}..{outline.yMax}")
check(keycap_heights == {1000}, f"keycap heights = {sorted(keycap_heights)}")

# Every standalone glyph SVG and sprite symbol uses the same 62-unit height.
svg_slot_heights = set()
for svg_path in (OUT / "glyphs").glob("U+*/*.svg"):
    match = re.search(r'<svg[^>]*\bheight="([0-9.]+)"', svg_path.read_text(encoding="utf-8"))
    check(match is not None, f"no height in {svg_path}")
    if match:
        svg_slot_heights.add(float(match.group(1)))
check(svg_slot_heights == {62.0}, f"glyph SVG heights = {sorted(svg_slot_heights)}")
sprite_heights = {float(m.group(1)) for m in re.finditer(r'<symbol[^>]*viewBox="0 0 [0-9.]+ ([0-9.]+)"', sprite)}
check(sprite_heights == {62.0}, f"sprite viewBox heights = {sorted(sprite_heights)}")
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
    for required in ["README.md", "OFL.txt", "OFL-JetBrainsMono.txt",
                     "demo.html", "demo-preview.png",
                     "KeycapTight-Regular.woff2", "glyphs/index.csv",
                     "keycap-tight-icons.csv", "keycap-tight-icons.svg",
                     "keycap-tight-icons.png", "keycap-tight-software-icons.csv",
                     "keycap-tight-hardware-icons.csv", "keycap-tight-text-map.csv"]:
        check(required in names, f"zip missing {required}")
    check(sum(n.startswith("glyphs/U+") and n.endswith(".svg") for n in names) == 95,
          "zip glyph svg count")

if errors:
    print("INVALID")
    for err in errors:
        print(" -", err)
    raise SystemExit(1)

print("ALL VALID")
print(f"101 physical keys -> 83 keycaps + 12 icons, 95 glyph folders, {len(names)} zip files")
print(f"font: {len(cmap)} cmap entries ({len(cmap) - 62} PUA + 62 ASCII aliases), {font['head'].unitsPerEm} upem")
