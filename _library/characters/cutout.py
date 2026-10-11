"""Remove the plain white background from a library image.
Usage: python3 cutout.py in.jpg out.png [--keep x,y ...] [--min-area 2500] [--max 900]
Removes the white background plus enclosed white gaps of at least --min-area pixels
(small white details such as eye whites and highlights stay).
--keep x,y : pixel coordinates (in the 2048px original) of large white areas to KEEP (teeth, big eyes, paper...)."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage

args = sys.argv[1:]
src, dst = args[0], args[1]
keep = [tuple(map(int, args[i + 1].split(","))) for i, a in enumerate(args) if a == "--keep"]
mx = int(args[args.index("--max") + 1]) if "--max" in args else 900
min_area = int(args[args.index("--min-area") + 1]) if "--min-area" in args else 2500

a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
mn = a.min(axis=2)
lab, k = ndimage.label(mn >= 236)
keep_ids = {lab[y, x] for x, y in keep} - {0}
sizes = ndimage.sum(np.ones_like(mn), lab, range(1, k + 1))
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
ids = [i for i in range(1, k + 1) if i not in keep_ids and (i in border or sizes[i - 1] >= min_area)]
bg = np.isin(lab, ids)
band = ndimage.binary_dilation(bg, iterations=3) & ~bg
alpha = np.ones(mn.shape, np.float32)
alpha[bg] = 0
soft = np.clip((255 - mn) / 70, 0, 1)
alpha[band] = np.minimum(alpha[band], soft[band])
al = alpha[..., None]
rgb = np.clip(np.where(al > 0.01, (a - (1 - al) * 255) / np.maximum(al, 0.01), 0), 0, 255)
img = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), "RGBA")
x0, y0, x1, y1 = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
img = img.crop((max(0, x0 - 24), max(0, y0 - 24), min(img.width, x1 + 24), min(img.height, y1 + 24)))
img.thumbnail((mx, mx), Image.LANCZOS)
img.save(dst, optimize=True)
print("saved", dst, img.size)
