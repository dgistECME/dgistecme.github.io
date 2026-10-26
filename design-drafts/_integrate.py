"""Add a batch of new artboards everywhere (canvas page, payload, site/design-drafts gallery + viewer, review board, README).

Usage: python _integrate.py batch.json
batch.json = {"page_id": "page-11", "page_name": "...", "group": "갤러리 그룹 제목", "brief": "캔버스 메모",
              "items": [{"file": "DirectionAD.dc.html", "title": "AD · ...", "h": 2400, "readme": "짧은 설명"}]}
If page_id / group already exist, the items are APPENDED to them (existing artboards kept);
then "brief_append" (optional) is added to the page's note instead of replacing it.
Requires each <file> and its .png (from _shot.py) to exist in design/.
"""
import json, re, shutil, subprocess, sys, pathlib

D = pathlib.Path(__file__).parent
S = D.parent / 'site' / 'design-drafts'
b = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
items = b['items']
new_files = {it['file'] for it in items}

# canvas.json
c = json.loads((D / 'canvas.json').read_text(encoding='utf-8'))
aid = b['page_id'] + '-brief'
page_exists = any(p['id'] == b['page_id'] for p in c['pages'])
if page_exists:
    c['artboards'] = [a for a in c['artboards'] if not (a['page'] == b['page_id'] and a['file'] in new_files)]
    on_page = [a for a in c['artboards'] if a['page'] == b['page_id']]
    x0 = max((a['x'] for a in on_page), default=-1560) + 1560
    idx = c['artboards'].index(on_page[-1]) + 1 if on_page else 1
    for n, it in enumerate(items):
        c['artboards'].insert(idx + n, {'file': it['file'], 'x': x0 + n * 1560, 'y': 0, 'w': 1440,
                                        'h': it['h'], 'title': it['title'], 'page': b['page_id']})
    ann = next((a for a in c['annotations'] if a['id'] == aid), None)
    if ann and b.get('brief_append') and b['brief_append'] not in ann['text']:
        ann['text'] = ann['text'].rstrip() + '\n' + b['brief_append']
else:
    c['pages'].insert(1, {'id': b['page_id'], 'name': b['page_name']})
    for n, it in enumerate(items):
        c['artboards'].insert(1 + n, {'file': it['file'], 'x': n * 1560, 'y': 0, 'w': 1440,
                                      'h': it['h'], 'title': it['title'], 'page': b['page_id']})
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

# gallery + viewer: drafts.json is the source; regenerate both pages
dj = S / 'drafts.json'; data = json.loads(dj.read_text(encoding='utf-8'))
entries = [{'file': it['file'], 'title': it['title'], 'desc': it['readme']} for it in items]
grp = next((g for g in data['groups'] if g['name'] == b['group']), None)
if grp:
    have = {x['file'] for x in grp['items']}
    grp['items'] += [e for e in entries if e['file'] not in have]
else:
    data['groups'].insert(1, {'name': b['group'], 'items': entries})
dj.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
subprocess.run([sys.executable, str(S / '_gallery.py')], check=True)
total = sum(len(g['items']) for g in data['groups'])

# review board (older decision page)
rp = S / 'review.html'; r = rp.read_text(encoding='utf-8')
todo = [it for it in items if f'href="{it["file"]}"' not in r]
if todo:
    cards = ''.join(card(it) for it in todo)
    m = re.search(r'<h3>' + re.escape(b['group']) + r'( \(최신\))?</h3><div class="grid">', r)
    if m:
        r = r[:m.end()] + cards + r[m.end():]
    else:
        r = r.replace('(최신)</h3>', '</h3>')
        i = r.index('</h2>', r.index('② 판단 대기')) + len('</h2>')
        r = r[:i] + f'<h3>{b["group"]} (최신)</h3><div class="grid">{cards}</div>' + r[i:]
    r = re.sub(r'(② 판단 대기 디자인<span class="badge">)(\d+)', lambda mm: mm.group(1) + str(int(mm.group(2)) + len(todo)), r)
rp.write_text(r, encoding='utf-8')

# README table rows on top
md = S / 'README.md'; t = md.read_text(encoding='utf-8')
rows = ''.join(f'| `{it["file"]}` | {it["title"]} ({it["readme"]}) | {b["group"]} |\n' for it in items if f'`{it["file"]}`' not in t)
if rows:
    i = t.index('| `', t.index('|---|'))
    t = t[:i] + rows + t[i:]
md.write_text(t, encoding='utf-8')
print('integrated', len(items), 'artboards; gallery total', total)
