"""Builds every character image a worksheet template needs, straight from the library.

In template.html, reference images like:  img/f/09-lucy-talking-right-lav.jpg
  <library file name without .jpg> - <background> .jpg
Backgrounds: w (white), lav (#F1EDF8), peach (#FDEDE5), night (#1B2147), sage (#D7E7DD), teal (#E3F0F3)
Each image is cut out of its white background (keeping teeth/eyes via _library/characters/cutout-keeps.json),
resized and flattened onto that background colour as a JPEG, which keeps the PDF small (about 1.5 MB).

Usage (from the repo root):  python3 _source/tools/prepare_images.py _source/<slug> [quality]
(quality = JPEG quality, default 90; use 84–86 if the PDF gets close to 2 MB – delete img/f first to rebuild)
Images that the template no longer uses are deleted, so you can start by copying an older worksheet folder.
"""
import json, re, subprocess, sys, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
LIB = ROOT / "_library" / "characters"
BG = {"w": "#FFFFFF", "lav": "#F1EDF8", "peach": "#FDEDE5", "night": "#1B2147", "sage": "#D7E7DD", "teal": "#E3F0F3"}

folder = pathlib.Path(sys.argv[1]).resolve()
Q = int(sys.argv[2]) if len(sys.argv) > 2 else 90
html = (folder / "template.html").read_text()
(folder / "img" / "f").mkdir(parents=True, exist_ok=True)
keeps = json.loads((LIB / "cutout-keeps.json").read_text())
refs = sorted(set(re.findall(r'img/f/([\w-]+)-(w|lav|peach|night|sage|teal)\.jpg', html)))
for name, bg in refs:
    out = folder / "img" / "f" / f"{name}-{bg}.jpg"
    if out.exists():
        continue
    png = folder / "img" / f"{name}.png"
    if not png.exists():
        src = LIB / f"{name}.jpg"
        if not src.exists():
            sys.exit(f"Missing library image: {src.name}")
        extra = keeps.get(src.name, "").split()
        mx = "820" if name.startswith("30-") else "440"
        subprocess.run([sys.executable, str(LIB / "cutout.py"), str(src), str(png), "--max", mx, *extra], check=True)
    im = Image.open(png).convert("RGBA")
    base = Image.new("RGBA", im.size, BG[bg]); base.alpha_composite(im)
    base.convert("RGB").save(out, quality=Q, subsampling=0, optimize=True)
    print("made", out.relative_to(ROOT))
used_jpg = {f"{n}-{b}.jpg" for n, b in refs}
used_png = {f"{n}.png" for n, _ in refs} | {"qr.png"}
for f in (folder / "img" / "f").glob("*.jpg"):
    if f.name not in used_jpg:
        f.unlink(); print("removed unused", f.name)
for f in (folder / "img").glob("*.png"):
    if f.name not in used_png:
        f.unlink(); print("removed unused", f.name)
print(len(refs), "image(s) ready")
