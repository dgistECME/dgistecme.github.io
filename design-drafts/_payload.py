"""Rewrite the canvas payload doc from files on disk: python _payload.py <file.dc.html ...>"""
import json, sys, pathlib
D = pathlib.Path(__file__).parent
p = D / 'ecme-lab-homepage.html'
s = p.read_text(encoding='utf-8')
tag = '<script type="application/json" id="appifact-doc">'
i = s.index(tag) + len(tag)
doc, j = json.JSONDecoder().raw_decode(s, i)
assert s[j:j+9] == '</script>', s[j:j+40]
for f in sys.argv[1:] + ['canvas.json']:
    doc['content']['files'][f] = (D / f).read_text(encoding='utf-8')
enc = json.dumps(doc, ensure_ascii=False).replace('<', chr(92) + 'u003c')
assert '</script' not in enc
s = s[:i] + enc + s[j:]
p.write_text(s, encoding='utf-8')
# self-check: round-trips and no raw '<' inside the doc
doc2, _ = json.JSONDecoder().raw_decode(s, s.index(tag) + len(tag))
assert doc2['content']['files'].keys() == doc['content']['files'].keys()
print('ok', len(doc2['content']['files']), 'files')
