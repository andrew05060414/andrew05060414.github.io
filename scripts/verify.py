"""Check publication contracts on the actual rendered artifact before deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json, re, struct

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT/'dist'
BASE = 'https://andrew05060414.github.io'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.elements=[]
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        self.elements.append((tag,dict(attrs)))

def verify():
    data=json.loads((ROOT/'content/site.json').read_text(encoding='utf-8'))
    assert set(data['TX']['en']) == set(data['TX']['zh']), 'Bilingual content keys differ'
    assert sum(t[1] for t in data['TIERS']) == 665, 'Snapshot classification total changed'
    private_links=('andrew05060414/pxread','andrew05060414/antiochus','andrew05060414/chronicle')
    for route,lang in [('','en'),('zh/','zh-CN')]:
        text=(OUT/route/'index.html').read_text(encoding='utf-8')
        p=Page(text)
        assert '{{' not in text and '{%' not in text, 'Unrendered template syntax'
        assert '<sc-' not in text and '<x-dc' not in text and 'support.js' not in text, 'Design runtime leaked'
        assert len([x for x in p.elements if x[0]=='h1']) == 1, 'Expected one H1'
        assert dict(next(x for x in p.elements if x[0]=='html')[1])['lang'] == lang
        ids=[a['id'] for _,a in p.elements if 'id' in a]
        assert len(ids)==len(set(ids)), 'Duplicate IDs'
        assert set(data['IDS']).issubset(ids), 'Missing file section'
        assert len([a for _,a in p.elements if 'f' in a.get('class','').split()]) == 665
        canonical=next(a['href'] for _,a in p.elements if a.get('rel')=='canonical')
        assert canonical==BASE+'/'+route, 'Wrong canonical URL'
        for tag,a in p.elements:
            for key in ('href','src'):
                value=a.get(key,'')
                if not value: continue
                assert not any(repo in value for repo in private_links), 'Private repository linked'
                u=urlsplit(value)
                if value.startswith('#'):
                    assert value[1:] in ids, f'Broken anchor {value}'
                if not u.scheme and u.path:
                    target=OUT/u.path.lstrip('/') if value.startswith('/') else OUT/route/u.path
                    assert target.exists(), f'Missing asset or route: {value}'
            assert not any(k.startswith('on') for k in a), 'Inline event handler'
        assert 'mailto:andrewwangmail@gmail.com' in text
        assert '2026-10-28' in text
    blocked=[r'[A-Z]:[\\/](?:Users|Andrew|Data|Temp)',r'\b(?:127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+)\b',
             r'\b(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}',r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----']
    for base in (ROOT/'content',ROOT/'templates',OUT):
        for path in base.rglob('*'):
            if path.is_file() and path.suffix in ('.html','.js','.css','.json','.xml','.txt'):
                text=path.read_text(encoding='utf-8')
                for pattern in blocked:
                    assert not re.search(pattern,text,re.I), f'Publication privacy check failed: {path.name}'
    card=OUT/'assets/social-card.png'
    header=card.read_bytes()[:24]
    assert header[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',header[16:24])==(1200,630), 'Social card must be a real 1200×630 PNG'
    print('PASS: bilingual pages, snapshots, links, local assets, semantics, publication privacy, and social image')

if __name__=='__main__':
    verify()
