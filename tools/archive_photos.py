"""Move photo-gallery images of old years to the separate media repo (own 1 GB Pages limit).

usage: python tools/archive_photos.py <last-year-to-move> <media-repo-checkout>
  e.g. python tools/archive_photos.py 2023 ../../media

Moves public/img/{full,thumb}/<stem>.webp of photos.yaml posts with year <= given year
(skipping any image also used elsewhere on the site) into <media>/img/{full,thumb}/,
and adds the stems to src/data/archived.json, which src/lib/img.ts serves from
https://dgistecme.github.io/media/. Push the media repo FIRST, check it is live, then push this site.
"""
import json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "src/data"


def main(last_year: int, media: Path):
    m = json.loads((DATA / "images.json").read_text(encoding="utf-8"))
    stem = lambda u: m.get(u) or (Path(u).stem if Path(u).suffix == ".webp" else None)
    photos = (DATA / "photos.yaml").read_text(encoding="utf-8")
    old = set()
    for post in re.split(r"(?m)^- year: ", photos)[1:]:
        if int(post.split("\n")[0].strip().strip("'\"")) <= last_year:
            old |= {stem(u) for u in re.findall(r"uri: (\S+)", post)} - {None}
    newer = "\n".join(p for p in re.split(r"(?m)^- year: ", photos)[1:] if int(p.split("\n")[0].strip().strip("'\"")) > last_year)
    elsewhere = newer + "".join(p.read_text(encoding="utf-8") for p in DATA.glob("*.yaml") if p.name != "photos.yaml")
    elsewhere += re.search(r"(?m)^profile_image: .*", photos).group(0)
    used = {stem(u) for u in re.findall(r"[\w~.-]+\.(?:jpe?g|png|webp|gif)", elsewhere)} - {None}
    move = sorted(old - used)
    archived = set(json.loads((DATA / "archived.json").read_text(encoding="utf-8"))) if (DATA / "archived.json").exists() else set()
    n = 0
    for s in move:
        for size in ("full", "thumb"):
            src = ROOT / f"public/img/{size}/{s}.webp"
            if src.exists():
                dst = media / f"img/{size}/{s}.webp"; dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(src, dst); n += 1
        archived.add(s)
    (DATA / "archived.json").write_text(json.dumps(sorted(archived), indent=1) + "\n", encoding="utf-8")
    print(f"{len(move)} images ({n} files) moved to {media}; archived.json has {len(archived)} stems")


if __name__ == "__main__":
    main(int(sys.argv[1]), Path(sys.argv[2]).resolve())
