"""Makes the website images for a finished worksheet PDF.

Usage (from the repo root):
  python3 _source/tools/site_images.py <slug> <preview page> <preview page> <preview page>
Example:
  python3 _source/tools/site_images.py talk-to-strangers 5 6 9
Writes <slug>/cover.webp, cover.jpg, og.jpg and page<N>.webp (the PDF must already be in <slug>/).
"""
import subprocess, sys, pathlib, tempfile, glob
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
slug, pages = sys.argv[1], [int(p) for p in sys.argv[2:]]
out = ROOT / slug
pdf = next(out.glob("*.pdf"))
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["pdftoppm", "-r", "150", "-png", str(pdf), str(tmp / "p")], check=True)
files = sorted(glob.glob(str(tmp / "p-*.png")))

def page(n):
    return Image.open(files[n - 1]).convert("RGB")

def save(im, path, w, fmt, q):
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if fmt == "WEBP":
        im.save(path, "WEBP", quality=q, method=6)
    else:
        im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
    return im

save(page(1), out / "cover.webp", 1200, "WEBP", 84)
save(page(1), out / "cover.jpg", 900, "JPEG", 82)
big = page(1).resize((1200, round(page(1).height * 1200 / page(1).width)), Image.LANCZOS)
big.crop((0, 0, 1200, 630)).save(out / "og.jpg", quality=82, optimize=True)
for n in pages:
    save(page(n), out / f"page{n}.webp", 640, "WEBP", 80)
print("site images ready in", out.relative_to(ROOT), "previews:", [f"page{n}.webp" for n in pages])
