"""e-Stat 衛生行政報告例(00450027) から「犬の登録申請数」表の一覧を取得し CSV をDLする"""
import re, time, sys, os, requests
from bs4 import BeautifulSoup
OUT = '/home/user/playbook/pet-data/raw/mhlw/estat'
H = {'User-Agent': 'Mozilla/5.0'}
q = '狂犬病'
found = {}
for page in range(1, 10):
    url = f'https://www.e-stat.go.jp/stat-search/files?page={page}&query={q}&layout=dataset&toukei=00450027&metadata=1&data=1'
    r = requests.get(url, headers=H, timeout=60); time.sleep(2)
    s = BeautifulSoup(r.text, 'html.parser')
    new = 0
    for a in s.find_all('a', href=re.compile('file-download')):
        sid = re.search(r'statInfId=(\d+)', a['href']).group(1)
        p = a.find_parent('article')
        tx = re.sub(r'\s+', ' ', p.get_text(' ', strip=True))
        if '犬の登録申請数' not in tx or sid in found: continue
        m = re.search(r'調査年月 (\d{4})年(度?)', tx)
        found[sid] = (m.group(1) if m else '', m.group(2) if m else '', tx[:300]); new += 1
    print(page, new, file=sys.stderr)
    if new == 0: break
with open(os.path.join(OUT, 'list.tsv'), 'w') as f:
    for sid, (y, d, tx) in sorted(found.items(), key=lambda x: x[1][0]):
        f.write(f'{sid}\t{y}\t{d}\t{tx}\n')
for sid, (y, d, tx) in found.items():
    fn = os.path.join(OUT, f'{y}{d}_{sid}.csv')
    if os.path.exists(fn): continue
    url = f'https://www.e-stat.go.jp/stat-search/file-download?statInfId={sid}&fileKind=1'
    r = requests.get(url, headers=H, timeout=120); time.sleep(2)
    open(fn, 'wb').write(r.content)
    open(fn + '.meta.txt', 'w').write(f'URL: {url}\n取得日: 2026-11-02\nHTTPステータス: {r.status_code}\n表: {tx}\n')
    print(sid, y, d, r.status_code, len(r.content), file=sys.stderr)
