"""Rebuild every deliverable from a clean dist directory.

Run with the bundled Python:
    python build_all.py

The source tree is work/; all generated files go to dist/.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "dist"
PY = sys.executable
NODE = os.environ.get("NODE_BIN", "node")


def run(args, label):
    print(f"\n== {label} ==")
    subprocess.run(args, cwd=HERE, check=True)


def screenshot_demo():
    candidates = [
        os.environ.get("EDGE_BIN"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    edge = next((p for p in candidates if p and Path(p).exists()), None)
    if not edge:
        print("\n== demo screenshot ==\nEdge not found; keeping existing demo-preview.png")
        return
    print("\n== demo screenshot ==")
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run([
            edge,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--window-size=1440,1500",
            "--virtual-time-budget=4000",
            f"--user-data-dir={profile}",
            f"--screenshot={OUT / 'demo-preview.png'}",
            (OUT / "demo.html").resolve().as_uri(),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    for script, label in [
        ("src/build_svg.py", "SVG sprite, specimen, per-character folders"),
        ("src/build_font.py", "TTF / WOFF2 + font proofs"),
        ("src/build_mapping.py", "JSON / CSV mapping"),
        ("src/build_demo.py", "live demo"),
    ]:
        run([PY, str(HERE / script)], label)

    run([NODE, str(HERE / "render_chars.js"), str(OUT / "glyphs")], "glyph PNG previews")
    run([NODE, str(HERE / "render.js"),
         str(OUT / "keycap-tight-icons.svg"),
         str(OUT / "keycap-tight-icons.png"), "1100"], "system icon sheet PNG")
    run([NODE, str(HERE / "render.js"),
         str(OUT / "keycap-tight-specimen.svg"),
         str(OUT / "keycap-tight-specimen.png"), "2200"], "specimen PNG")

    screenshot_demo()
    run([PY, str(HERE / "build_package.py")], "README, CSS, OFL and ZIP package")
    run([PY, str(HERE / "validate.py")], "validation")

    for cache in HERE.rglob("__pycache__"):
        shutil.rmtree(cache, ignore_errors=True)


if __name__ == "__main__":
    main()
