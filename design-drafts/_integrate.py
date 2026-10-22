"""Add a batch of new artboards everywhere (canvas page, payload, site/design-drafts gallery, review board, README).

Usage: python _integrate.py batch.json
batch.json = {"page_id": "page-11", "page_name": "...", "group": "갤러리 그룹 제목", "brief": "캔버스 메모",
              "items": [{"file": "DirectionAD.dc.html", "title": "AD · ...", "h": 2400, "readme": "짧은 설명"}]}
Requires each <file> and its .png (from _shot.py) to exist in design/.
"""
import json, re, shutil, subprocess, sys, pathlib

D = pathlib.Path(__file__).parent
S = D.parent / 'site' / 'design-drafts'
b = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
items = b['items']

# canvas.json: new page first after Final, launch on it
c = json.loads((D / 'canvas.json').read_text(encoding='utf-8'))
c['pages'] = [p for p in c['pages'] if p['id'] != b['page_id']]
c['pages'].insert(1, {'id': b['page_id'], 'name': b['page_name']})
c['artboards'] = [a for a in c['artboards'] if a['page'] != b['page_id']]
for n, it in enumerate(items):
    c['artboards'].insert(1 + n, {'file': it['file'], 'x': n * 1560, 'y': 0, 'w': 1440,
                                  'h': it['h'], 'title': it['title'], 'page': b['page_id']})
aid = b['page_id'] + '-brief'
c['annotations'] = [a for a in c['annotations'] if a['id'] != aid]
c['annotations'].insert(1, {'id': aid, 'x': 0, 'y': -440, 'w': 880, 'page': b['page_id'], 'text': b['brief']})
c['launch'] = {'view': 'canvas', 'page': b['page_id']}
(D / 'canvas.json').write_text(json.dumps(c, ensure_ascii=False, indent=2), encoding='utf-8')

# payload (escaping + self-check live in _payload.py)
subprocess.run([sys.executable, str(D / '_payload.py')] + [it['file'] for it in items], check=True)

# site/design-drafts copies
for it in items:
    shutil.copy(D / it['file'], S / it['file'])
    shutil.copy(D / it['file'].replace('.dc.html', '.png'), S / it['file'].replace('.dc.html', '.png'))
for f in ['canvas.json', '_payload.py', '_shot.py', '_integrate.py']:
    shutil.copy(D / f, S / f)

def card(it):
    f = it['file']
    return (f'<a class="card" href="{f}" target="_blank"><div class="thumb"><img src="{f[:-8]}.png" '
            f'loading="lazy" alt="{it["title"]}"></div><div class="cap">{it["title"]}<span>{f} ↗</span></div></a>')
cards = ''.join(card(it) for it in items)
marker = items[0]['title']

# gallery: new group right after the live one
ip = S / 'index.html'; h = ip.read_text(encoding='utf-8')
if marker not in h:
    h = h.replace('(최신)</h2>', '</h2>')  # previous "latest" group loses the tag
    i = h.index('</div>', h.index('<h2>적용 중')) + len('</div>')
    h = h[:i] + f'<h2>{b["group"]} (최신)</h2><div class="grid">{cards}</div>' + h[i:]
    total = h.count('class="card"')
    h = re.sub(r'\d+안', f'{total}안', h)
ip.write_text(h, encoding='utf-8')

# review board: first group under "② 판단 대기"
rp = S / 'review.html'; r = rp.read_text(encoding='utf-8')
if marker not in r:
    r = r.replace('(최신)</h3>', '</h3>')
    i = r.index('</h2>', r.index('② 판단 대기')) + len('</h2>')
    r = r[:i] + f'<h3>{b["group"]} (최신)</h3><div class="grid">{cards}</div>' + r[i:]
    r = re.sub(r'(② 판단 대기 디자인<span class="badge">)(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + len(items)), r)
rp.write_text(r, encoding='utf-8')

# README table rows on top
md = S / 'README.md'; t = md.read_text(encoding='utf-8')
if marker not in t:
    rows = ''.join(f'| `{it["file"]}` | {it["title"]} ({it["readme"]}) | {b["group"]} |\n' for it in items)
    i = t.index('| `', t.index('|---|'))
    t = t[:i] + rows + t[i:]
md.write_text(t, encoding='utf-8')
print('integrated', len(items), 'artboards; gallery total', h.count('class="card"'))
