"""Convert photos for the site.

usage: python tools/add_images.py <name-prefix> <file-or-folder> [more files...] [--no-thumb] [--max 1600]

Writes public/img/full/<prefix>-N.webp (and public/img/thumb/<prefix>-N.webp) and prints YAML lines to paste.
Single file -> name is exactly <prefix>.webp.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
FULL, THUMB = ROOT / "public/img/full", ROOT / "public/img/thumb"
EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif", ".bmp", ".tif", ".tiff"}


def convert(src: Path, name: str, max_px: int, thumb: bool):
    im = ImageOps.exif_transpose(Image.open(src))
    im = im.convert("RGBA" if ("A" in im.getbands() or "transparency" in im.info or im.mode == "P") else "RGB")
    for folder, size, q in ((FULL, max_px, 82), (THUMB, 480, 78)):
        if folder is THUMB and not thumb:
            continue
        w = im.copy(); w.thumbnail((size, size), Image.LANCZOS)
        folder.mkdir(parents=True, exist_ok=True)
        w.save(folder / f"{name}.webp", "WEBP", quality=q, method=6)
    return f"{name}.webp"


if __name__ == "__main__":
    argv = sys.argv[1:]
    thumb = "--no-thumb" not in argv
    max_px = 1600
    if "--max" in argv:
        i = argv.index("--max"); max_px = int(argv[i + 1]); del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    prefix, inputs = args[0], args[1:]
    files = []
    for i in inputs:
        p = Path(i)
        files += sorted(f for f in p.iterdir() if f.suffix.lower() in EXT) if p.is_dir() else [p]
    for n, f in enumerate(files, 1):
        name = prefix if len(files) == 1 else f"{prefix}-{n}"
        out = convert(f, name, max_px, thumb)
        print(f"  - uri: {out}\n    alt: null")
