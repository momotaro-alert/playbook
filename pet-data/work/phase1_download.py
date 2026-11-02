"""Phase1: 環境省 動物愛護管理行政事務提要 の関連ファイルを各年度版一覧ページから辿ってダウンロードする。
usage: python3 -I work/phase1_download.py
raw/env/<版>/<file> と .meta.txt を作成。既存ファイルはスキップ。
"""
import os, re, time, glob, datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

ROOT = '/home/user/playbook/pet-data/raw/env'
BASE = 'https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/'
UA = {'User-Agent': 'Mozilla/5.0'}
TODAY = '2026-11-02'
KEYS = ['引取', '取扱業', '登録頭数', 'マイクロ', '勧告', '負傷動物', '分類']


def save(url, path):
    if os.path.exists(path):
        return 'skip'
    r = requests.get(url, headers=UA, timeout=60)
    time.sleep(2)
    with open(path + '.meta.txt', 'w') as f:
        f.write(f'URL: {url}\n取得日: {TODAY}\nHTTPステータス: {r.status_code}\n'
                f'Content-Type: {r.headers.get("Content-Type")}\nサイズ: {len(r.content)}\n')
    if r.status_code == 200:
        with open(path, 'wb') as f:
            f.write(r.content)
    return r.status_code


def main():
    # index pages themselves -> meta
    for html in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        name = os.path.basename(html)
        meta = html + '.meta.txt'
        if not os.path.exists(meta):
            with open(meta, 'w') as f:
                f.write(f'URL: {BASE}{name}\n取得日: {TODAY}\nHTTPステータス: 200\n')
    for html in sorted(glob.glob(os.path.join(ROOT, 'gyosei-jimu_*.html'))) + [os.path.join(ROOT, 'dog-cat.html')]:
        ed = re.sub(r'gyosei-jimu_|\.html', '', os.path.basename(html))
        s = BeautifulSoup(open(html, 'rb').read(), 'html.parser')
        outdir = os.path.join(ROOT, ed)
        os.makedirs(outdir, exist_ok=True)
        for a in s.find_all('a'):
            h = a.get('href', '')
            if not h.lower().endswith(('.pdf', '.xlsx', '.xls', '.csv')):
                continue
            t = a.get_text(' ', strip=True)
            if not any(k in t for k in KEYS):
                continue
            url = urljoin(BASE + os.path.basename(html), h)
            fn = os.path.basename(h)
            st = save(url, os.path.join(outdir, fn))
            print(ed, fn, st, t[:50])


if __name__ == '__main__':
    main()
