#!/usr/bin/env python3
"""Phase 4: ペットミー (petmi.jp) 全国一覧ページ（犬種/猫種別、都道府県を絞らない）をページ送りで取得し、
カード情報をパースして JSONL に保存する。

  python3 -I work/phase4_fetch_petmi.py [--kinds dog/kind-64,cat/kind-92] [--max-pages N]

- 1リクエストごとに 2.5 秒待機。User-Agent は研究目的を明示。
- 各犬種の 1 ページ目 HTML はサンプルとして raw/prices/ に .meta.txt 付きで保存。
- 出力: raw/prices/petmi_listings.jsonl（1行=1カード）, raw/prices/petmi_fetchlog.tsv
- robots.txt (確認 2026-11-02): Disallow は /api/, /pvt/, /shop-admin/ のみ。一覧ページは対象外。
- 利用規約 https://petmi.jp/terms/ 第4条にスクレイピング禁止条項なし（運営阻害行為は禁止→低頻度で実施）。
"""
import argparse, datetime, json, math, os, re, sys, time
import requests
from bs4 import BeautifulSoup

ROOT = '/home/user/playbook/pet-data'
RAW = os.path.join(ROOT, 'raw', 'prices')
UA = 'Mozilla/5.0 (research; contact via site)'
WAIT = 2.5
FETCH_DATE = datetime.date.today().isoformat()

# 対象品種: (path, 依頼上の品種名)
KINDS = [
    ('dog/kind-64', 'トイ・プードル'),
    ('dog/kind-5', 'チワワ'),
    ('dog/kind-56', 'ミニチュア・ダックスフンド'),
    ('dog/kind-127', 'ポメラニアン'),
    ('dog/kind-166', '柴犬'),
    ('dog/kind-19', 'ミニチュア・シュナウザー'),
    ('dog/kind-47', 'フレンチ・ブルドッグ'),
    ('dog/kind-102', 'ヨークシャー・テリア'),
    ('dog/kind-55', 'マルチーズ'),
    ('dog/kind-33', 'シー・ズー'),
    ('dog/kind-140', 'ゴールデン・レトリーバー'),
    ('dog/kind-95', 'MIX（ハーフ）'),
    ('cat/kind-92', 'スコティッシュ・フォールド'),
    ('cat/kind-138', 'マンチカン'),
    ('cat/kind-177', 'ラグドール'),
    ('cat/kind-22', 'ブリティッシュ・ショートヘア'),
    ('cat/kind-51', 'ミヌエット'),
    ('cat/kind-91', 'アメリカン・ショートヘア'),
    ('cat/kind-99', 'エキゾチック'),
    ('cat/kind-24', 'ノルウェージャン'),
]

sess = requests.Session()
sess.headers['User-Agent'] = UA
_last = [0.0]


def get(url):
    dt = time.time() - _last[0]
    if dt < WAIT:
        time.sleep(WAIT - dt)
    for attempt in range(3):
        try:
            r = sess.get(url, timeout=40)
            _last[0] = time.time()
            if r.status_code in (429, 503):
                time.sleep(30 * (attempt + 1))
                continue
            return r
        except requests.RequestException as e:
            _last[0] = time.time()
            print('ERR', url, e, file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    return None


def total_count(html):
    m = re.search(r'([\d,]+)\s*頭', html)
    return int(m.group(1).replace(',', '')) if m else None


def parse_cards(html, animal, query_path, query_name, list_url):
    s = BeautifulSoup(html, 'html.parser')
    out = []
    for c in s.select('div.card'):
        a = c.select_one('.main a[href*="/detail/"]')
        if not a:
            continue
        rec = {
            'サイト': 'ペットミー',
            '犬/猫': animal,
            '対象品種': query_name,
            '検索kind': query_path,
            '掲載品種': (c.select_one('.kind').get_text(strip=True) if c.select_one('.kind') else ''),
            '掲載URL': 'https://petmi.jp' + a['href'],
            '一覧URL': list_url,
            '取得日': FETCH_DATE,
        }
        for row in c.select('.info .row'):
            lab = row.select_one('.label')
            lab = lab.get_text(strip=True) if lab else ''
            if 'price-row' in (row.get('class') or []):
                p = row.select_one('.price')
                t = row.select_one('.tax')
                rec['価格_表示'] = row.get_text('', strip=True)
                rec['価格'] = int(re.sub(r'[^\d]', '', p.get_text())) if p and re.search(r'\d', p.get_text()) else None
                rec['税区分'] = t.get_text(strip=True) if t else ''
            else:
                v = row.select_one('.value')
                rec[lab] = v.get_text(strip=True) if v else ''
        sn = c.select_one('.shop-name')
        if sn:
            lab = sn.select_one('.shop-label')
            rec['店舗ラベル'] = lab.get_text(strip=True) if lab else ''
            if lab:
                lab.extract()
            rec['店舗名'] = sn.get_text(strip=True)
        addr = c.select_one('.shop-panel .shop-row-value')
        rec['店舗所在地'] = addr.get_text(strip=True) if addr else ''
        rec['バッジ'] = [b.get_text(strip=True) for b in c.select('.badge')]
        rec['掲載経過'] = (c.select_one('.posted').get_text(strip=True) if c.select_one('.posted') else '')
        out.append(rec)
    return out


def save_sample(name, url, r):
    p = os.path.join(RAW, name)
    with open(p, 'wb') as f:
        f.write(r.content)
    with open(p + '.meta.txt', 'w', encoding='utf-8') as f:
        f.write(f'URL: {url}\n取得日: {FETCH_DATE}\nHTTPステータス: {r.status_code}\nUser-Agent: {UA}\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kinds', default='')
    ap.add_argument('--max-pages', type=int, default=100)
    a = ap.parse_args()
    kinds = KINDS if not a.kinds else [k for k in KINDS if k[0] in a.kinds.split(',')]
    os.makedirs(RAW, exist_ok=True)
    out_path = os.path.join(RAW, 'petmi_listings.jsonl')
    log_path = os.path.join(RAW, 'petmi_fetchlog.tsv')
    logf = open(log_path, 'a', encoding='utf-8')
    with open(out_path, 'a', encoding='utf-8') as out:
        for path, name in kinds:
            animal = '犬' if path.startswith('dog') else '猫'
            base = f'https://petmi.jp/{path}/'
            r = get(base)
            if r is None or r.status_code != 200:
                logf.write(f'{FETCH_DATE}\t{base}\t{getattr(r, "status_code", "ERR")}\t0\n'); logf.flush()
                continue
            save_sample(f'petmi_{path.replace("/", "_")}_p1.html', base, r)
            n = total_count(r.text)
            pages = min(math.ceil(n / 30) if n else 1, a.max_pages)
            print(f'{path} {name}: total={n} pages={pages}', flush=True)
            for pg in range(1, pages + 1):
                url = base if pg == 1 else f'{base}?page={pg}'
                if pg > 1:
                    r = get(url)
                if r is None:
                    logf.write(f'{FETCH_DATE}\t{url}\tERR\t0\n'); logf.flush()
                    continue
                recs = parse_cards(r.text, animal, path, name, url) if r.status_code == 200 else []
                for rec in recs:
                    rec['一覧総数'] = n
                    out.write(json.dumps(rec, ensure_ascii=False) + '\n')
                out.flush()
                logf.write(f'{FETCH_DATE}\t{url}\t{r.status_code}\t{len(recs)}\n'); logf.flush()
                if r.status_code != 200 or not recs:
                    print(f'  stop at page {pg}: status={r.status_code} cards={len(recs)}', flush=True)
                    break


if __name__ == '__main__':
    main()
