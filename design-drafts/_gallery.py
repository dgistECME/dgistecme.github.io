"""Build index.html (thumbnail gallery) and viewer.html (tabbed live viewer) from drafts.json.

drafts.json = {"groups": [{"name": "...", "items": [{"file": "X.dc.html", "title": "...", "desc": "..."}]}]}
Newest group goes right after the first ("적용 중 · 라이브") group.  Run:  python _gallery.py
"""
import html, json, pathlib

D = pathlib.Path(__file__).parent
groups = json.loads((D / 'drafts.json').read_text(encoding='utf-8'))['groups']
items = [dict(it, group=g['name']) for g in groups for it in g['items']]
files = [it['file'] for it in items]
assert len(files) == len(set(files)), 'duplicate draft'
missing = [f for f in files if not (D / f).exists()]
assert not missing, f'missing files: {missing}'
n = len(items)
esc = html.escape

# index.html — thumbnail gallery
CSS = ('body{margin:0;background:#f4f6f9;font-family:system-ui,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;color:#111;padding:32px 40px 60px}'
       'h1{font-size:24px;margin:0 0 6px}p.sub{color:#666;margin:0 0 28px;font-size:14px}'
       'h2{font-size:15px;letter-spacing:.06em;color:#555;margin:34px 0 12px}'
       '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}'
       '.card{display:block;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 4px 18px rgba(0,0,0,.07);color:inherit;text-decoration:none;transition:transform .2s,box-shadow .2s}'
       '.card:hover{transform:translateY(-4px);box-shadow:0 14px 34px rgba(0,0,0,.12)}'
       '.thumb{height:260px;overflow:hidden;background:#e9edf2}.thumb img{width:100%;display:block;object-fit:cover;object-position:top}'
       '.cap{padding:12px 14px;font-weight:600;font-size:14px;display:flex;justify-content:space-between;align-items:baseline;gap:8px}'
       '.cap span{font-weight:400;font-size:12px;color:#888;white-space:nowrap}'
       '.viewer{display:inline-block;margin-top:4px;padding:9px 16px;border-radius:10px;background:#111;color:#fff;text-decoration:none;font-weight:600;font-size:14px}')
parts = [f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         f'<title>ECME 홈페이지 디자인 초안 {n}안</title><style>{CSS}</style></head><body>'
         f'<h1>ECME LAB 홈페이지 디자인 초안 — {n}안</h1>'
         f'<p class="sub">카드 클릭 → 해당 안을 뷰어에서 열기(애니메이션 재생, ←/→로 넘김). 썸네일은 상단 부분만. '
         f'라이브 사이트: <a href="https://dgistecme.github.io/" target="_blank">dgistecme.github.io</a><br>'
         f'<a class="viewer" href="viewer.html">▶ 뷰어로 전체 넘겨보기</a></p>']
for gi, g in enumerate(groups):
    tag = ' (최신)' if gi == 1 else ''
    parts.append(f'<h2>{esc(g["name"])}{tag}</h2><div class="grid">')
    for it in g['items']:
        stem = it['file'][:-8]
        parts.append(f'<a class="card" href="viewer.html#{stem}"><div class="thumb"><img src="{stem}.png" loading="lazy" alt="{esc(it["title"])}"></div>'
                     f'<div class="cap">{esc(it["title"])}<span>{esc(it["file"])}</span></div></a>')
    parts.append('</div>')
parts.append('</body></html>')
(D / 'index.html').write_text(''.join(parts), encoding='utf-8')

# viewer.html — template + data
tpl = (D / '_viewer.tpl.html').read_text(encoding='utf-8')
assert '/*ITEMS*/[]' in tpl
(D / 'viewer.html').write_text(tpl.replace('/*ITEMS*/[]', json.dumps(items, ensure_ascii=False)).replace('{{COUNT}}', str(n)), encoding='utf-8')
print(f'index.html + viewer.html: {n} drafts, {len(groups)} groups')
