# Phase 3 共通ヘルパー（各 phase3_*.py から exec で読み込む。python3 -I でも動くよう import ではなく exec）
# 使い方: exec(open('/home/user/playbook/pet-data/work/phase3_common.py', encoding='utf-8').read())
import csv
import logging
import re
logging.getLogger('pdfminer').setLevel(logging.ERROR)
logging.getLogger('pdfplumber').setLevel(logging.ERROR)
import subprocess
import sys
from pathlib import Path

ROOT = Path('/home/user/playbook/pet-data')
RAW = ROOT / 'raw'
CLEAN = ROOT / 'clean'
DATE = '2026-11-02'
COLS = ['年度または暦年', '年', '動物', '項目', '値', '単位', '区分', '出典URL', '取得日', '備考']

_cache = {}
WARN = []


def text_of(rel):
    """raw/ 以下の相対パスからテキストを得る（HTML/PDF/TXT）。"""
    if rel in _cache:
        return _cache[rel]
    p = RAW / rel
    if p.suffix == '.pdf':
        t = ''
        try:
            import pdfplumber
            with pdfplumber.open(str(p)) as pdf:
                t = '\n'.join((pg.extract_text() or '') for pg in pdf.pages)
        except Exception as e:  # noqa
            t = ''
        try:
            t2 = subprocess.run(['pdftotext', '-layout', str(p), '-'], capture_output=True, text=True).stdout
        except Exception:
            t2 = ''
        t = t + '\n' + t2
    elif p.suffix in ('.html', '.htm'):
        from bs4 import BeautifulSoup
        s = BeautifulSoup(p.read_bytes(), 'html.parser')
        for x in s(['script', 'style', 'noscript']):
            x.decompose()
        t = s.get_text('\n')
        # Vue テンプレート等の属性内テキストも検索対象に含める
        t += '\n' + p.read_text(encoding='utf-8', errors='ignore')
    else:
        t = p.read_text(encoding='utf-8', errors='ignore')
    _cache[rel] = t
    return t


def norm(s):
    return re.sub(r'[\s　]+', '', s)


def check(rel, *evidence):
    t = norm(text_of(rel))
    for e in evidence:
        if norm(e) not in t:
            WARN.append(f'[根拠未検出] {rel}: {e}')


def url_of(rel):
    m = (RAW / (rel + '.meta.txt')).read_text(encoding='utf-8')
    return re.search(r'URL:\s*(\S+)', m).group(1)


def row(kind, year, animal, item, value, unit, cat, src, note='', ev=(), extra=None):
    """src は raw 相対パス（.meta.txt から URL を引く）か http で始まる URL。ev は raw 内に存在すべき根拠文字列。"""
    if not src or src.startswith('http'):
        url = src
    else:
        url = url_of(src)
        if ev:
            check(src, *ev)
    r = {'年度または暦年': kind, '年': year, '動物': animal, '項目': item, '値': value, '単位': unit,
         '区分': cat, '出典URL': url, '取得日': DATE, '備考': note}
    if extra:
        r.update(extra)
    return r


def write(name, rows, cols=None):
    cols = cols or COLS
    CLEAN.mkdir(exist_ok=True)
    with open(CLEAN / name, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in cols})
    print(f'wrote clean/{name}: {len(rows)} rows')


def finish():
    if WARN:
        print('\n'.join(WARN))
        print(f'WARN {len(WARN)} 件')
        sys.exit(1)
    print('根拠文字列チェック: すべて検出')
