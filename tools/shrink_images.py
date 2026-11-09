"""Safety net, run in CI before the build.

Any image in public/img that is too big (longer side over the limit, or over 1 MB)
is resized and re-encoded in place, same file name and format, so YAML references
keep working and the published site stays small even if an original photo was uploaded.
Images already within limits are never touched (no repeated quality loss).

This only protects the site. An original that was committed still sits in git history,
so the normal way to add photos is tools/add_images.py BEFORE committing.
"""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent / "public/img"
LIMITS = {"full": 2000, "thumb": 480}
MAX_BYTES = 1_000_000


def shrink(p: Path, max_px: int) -> bool:
    im = Image.open(p)
    fmt = im.format
    if fmt not in {"JPEG", "MPO", "PNG", "WEBP"} or getattr(im, "n_frames", 1) > 1:
        return False  # skip GIF/animated images
    if max(im.size) <= max_px and p.stat().st_size <= MAX_BYTES:
        return False
    before = p.stat().st_size
    im = ImageOps.exif_transpose(im)
    im.thumbnail((max_px, max_px), Image.LANCZOS)
    if fmt == "PNG":
        im.save(p, "PNG", optimize=True)
    elif fmt == "WEBP":
        im.save(p, "WEBP", quality=86, method=6)
    else:
        im.convert("RGB").save(p, "JPEG", quality=90, optimize=True, progressive=True)
    after = p.stat().st_size
    tag = "warning" if after > MAX_BYTES else "notice"
    print(f"::{tag}::{p.relative_to(ROOT.parent.parent)} {before // 1024} KB -> {after // 1024} KB "
          f"(original is in git history; use tools/add_images.py before committing)")
    return True


if __name__ == "__main__":
    n = 0
    for d in LIMITS:
        for p in sorted((ROOT / d).glob("*")):
            try:
                n += p.is_file() and shrink(p, LIMITS[d])
            except Exception as e:  # unreadable/non-image file: leave it alone
                print(f"::warning::skipped {p.name}: {e}")
    print(f"shrink_images: {n} file(s) resized")
