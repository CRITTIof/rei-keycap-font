"""Assemble release-root files and create KeycapTight-Windows.zip."""
import json
import shutil
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "src"))
sys.path.insert(0, str(HERE / "pydeps"))

import geometry as G
from data import PHYS, UNIQUE, ICONS, ALL_GLYPHS

OUT = G.OUT
ZIP = OUT / "KeycapTight-Windows.zip"


def copy(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


copy(HERE / "templates" / "README.md", OUT / "README.md")
copy(HERE / "templates" / "keycap-tight.css", OUT / "keycap-tight.css")
copy(HERE / "assets" / "OFL.txt", OUT / "OFL.txt")

# Keep the zip deterministic and exclude any previous archive.
files = sorted(
    p for p in OUT.rglob("*")
    if p.is_file() and p != ZIP and "__pycache__" not in p.parts
)
with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for path in files:
        zf.write(path, path.relative_to(OUT).as_posix())

# --- Validation -----------------------------------------------------------
char_dirs = sorted(p for p in (OUT / "字符").iterdir() if p.is_dir())
svg_files = list((OUT / "字符").glob("U+*/*.svg"))
json_files = list((OUT / "字符").glob("U+*/glyph.json"))
png_files = list((OUT / "字符").glob("U+*/preview.png"))
mapping = json.loads((OUT / "keycap-tight-mapping.json").read_text(encoding="utf-8"))

assert len(char_dirs) == len(ALL_GLYPHS) == 89, len(char_dirs)
assert len(svg_files) == 89, len(svg_files)
assert len(json_files) == 89, len(json_files)
assert len(mapping["keys"]) == len(PHYS) == 101, len(mapping["keys"])
assert len(mapping["glyphs"]) == len(UNIQUE) == 83, len(mapping["glyphs"])
assert len(mapping["icons"]) == len(ICONS) == 6, len(mapping["icons"])
assert ZIP.exists() and ZIP.stat().st_size > 0

print(f"glyph folders     : {len(char_dirs)} (83 keycaps + 6 icons)")
print(f"glyph SVGs        : {len(svg_files)}")
print(f"glyph JSON        : {len(json_files)}")
print(f"glyph previews    : {len(png_files)}")
print(f"mapping keys      : {len(mapping['keys'])}")
print(f"system icons      : {len(mapping['icons'])}")
print(f"zip files         : {len(files)}")
print(f"zip size          : {ZIP.stat().st_size:,} bytes")
print(f"zip               : {ZIP}")
