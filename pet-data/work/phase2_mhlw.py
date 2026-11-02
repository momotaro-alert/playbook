"""Phase 2 / 3-2: 厚労省 狂犬病予防法 登録頭数・注射頭数 + e-Stat 衛生行政報告例(新規登録申請数等)
入力: raw/mhlw/02.html, raw/mhlw/estat/*.csv
出力: clean/狂犬病_登録注射.csv
実行: python3 -I work/phase2_mhlw.py
"""
import csv, glob, io, os, re
from bs4 import BeautifulSoup

ROOT = '/home/user/playbook/pet-data'
GET = '2026-11-02'
MHLW_URL = 'https://www.mhlw.go.jp/bunya/kenkou/kekkaku-kansenshou10/02.html'
rows = []


def add(y, kind, animal, item, val, unit, cat, url, note=''):
    rows.append({'年': y, '年度または暦年': kind, '動物': animal, '項目': item, '値': val, '単位': unit,
                 '区分': cat, '出典URL': url, '取得日': GET, '備考': note})


def num(s):
    s = s.replace(',', '').strip()
    return int(s) if re.fullmatch(r'\d+', s) else None


# ---- 1) 厚労省ページ
html = open(f'{ROOT}/raw/mhlw/02.html', 'rb').read().decode('cp932')
soup = BeautifulSoup(html, 'html.parser')
era = None
base = {'昭和': 1925, '平成': 1988, '令和': 2018}
mhlw = {}
for tr in soup.find_all('tr'):
    c = [x.get_text(' ', strip=True) for x in tr.find_all(['td', 'th'])]
    if len(c) != 6 or not c[1] or num(c[1]) is None:
        continue
    lab = c[0]
    m = re.match(r'(昭和|平成|令和)', lab)
    if m:
        era = m.group(1)
    yy = re.search(r'(\d+|元)', lab.replace(' ', ''))
    n = 1 if yy.group(1) == '元' else int(yy.group(1))
    year = base[era] + n
    fy = year >= 1997  # ※2 平成9年度から年度単位
    kind = '年度' if fy else '暦年'
    notes = []
    if '※1' in lab:
        notes.append('※1 昭和60年4月から注射期間が半年→1年に変更。注射頭数は旧制度(1-3月)と新制度(4-12月)を含む')
    if '※3' in lab:
        notes.append('※3 東日本大震災の影響で岩手県陸前高田市・大槌町の1-3月分、宮城県(仙台市以外)、福島県相双保健福祉事務所管内を含まない')
    if '※4' in lab:
        notes.append('※4 予防注射頭数は茨城県の修正により衛生行政報告例と異なる')
    if year == 1997:
        notes.append('※2 平成9年度から年度単位の集計（平成8年までは暦年）')
    note = ' / '.join(notes)
    items = [('登録頭数', c[1], '年度末現在' if fy else '年末現在'), ('予防注射頭数', c[2], ''),
             ('抑留頭数', c[3], ''), ('返還頭数', c[4], ''), ('差引頭数（抑留-返還）', c[5], '')]
    for item, v, extra in items:
        add(year, kind, '犬', item, num(v), '頭', '実測', MHLW_URL, ' / '.join(x for x in [extra, note] if x))
    mhlw[year] = (num(c[1]), num(c[2]))

# ---- 2) e-Stat 衛生行政報告例 全国行
estat_check = []
for fn in sorted(glob.glob(f'{ROOT}/raw/mhlw/estat/*.csv')):
    base_name = os.path.basename(fn)
    if '1-3月' in base_name:
        continue  # 平成9年1-3月の端数期間は対象外（logに記載）
    meta = open(fn + '.meta.txt', encoding='utf-8').read()
    url = re.search(r'URL: (\S+)', meta).group(1)
    m = re.match(r'(\d{4})(度?)_', base_name)
    year, fy = int(m.group(1)), m.group(2) == '度'
    txt = open(fn, 'rb').read().decode('cp932')
    nat = None
    for r in csv.reader(io.StringIO(txt)):
        if r and re.sub(r'[\s　]', '', r[0]) == '全国':
            nat = r
            break
    v = [num(x) for x in nat[1:] if not re.fullmatch(r'\s*\d\)\s*', x)]  # 注記列(例 '1)')を除く
    kind = '年度' if fy else '暦年'
    src = '衛生行政報告例（e-Stat）'
    add(year, kind, '犬', '新規登録申請数', v[0], '件', '実測', url, f'{src} 全国計。登録申請数=狂犬病予防法4条の新規登録申請')
    add(year, kind, '犬', '犬の死亡届出件数', v[7], '件', '実測', url, f'{src} 全国計')
    if len(v) > 8 and v[8] is not None:
        add(year, kind, '犬', '登録の消除件数（死亡推定によるもの）', v[8], '件', '実測', url, f'{src} 全国計（令和6年度から追加の列）')
    # 1997-2011年度以外で厚労省ページに無い年(例 2025年度)は登録・注射も追加
    if year not in mhlw:
        add(year, kind, '犬', '登録頭数', v[1], '頭', '実測', url, f'{src} 全国計 年度末現在（厚労省年次推移ページ未掲載年）')
        add(year, kind, '犬', '予防注射頭数', v[2], '頭', '実測', url, f'{src} 全国計 予防注射済票交付数（厚労省年次推移ページ未掲載年）')
        add(year, kind, '犬', '抑留頭数', v[5], '頭', '実測', url, f'{src} 全国計（厚労省年次推移ページ未掲載年）')
        add(year, kind, '犬', '返還頭数', v[6], '頭', '実測', url, f'{src} 全国計（厚労省年次推移ページ未掲載年）')
    else:
        estat_check.append((year, mhlw[year][0], v[1], mhlw[year][1], v[2]))

# 猫: 制度なし
add('', '', '猫', '登録頭数・予防注射頭数・新規登録申請数', '', '', '実測', MHLW_URL,
    '猫には制度がない（狂犬病予防法の登録・予防注射義務は犬のみ）')

# 計算: 注射率（予防注射頭数/登録頭数）
by = {}
for r in rows:
    if r['動物'] == '犬' and r['項目'] in ('登録頭数', '予防注射頭数') and r['値'] is not None:
        by.setdefault((r['年'], r['年度または暦年']), {})[r['項目']] = (r['値'], r['出典URL'])
for (y, k), d in sorted(by.items()):
    if '登録頭数' in d and '予防注射頭数' in d:
        add(y, k, '犬', '注射率（予防注射頭数÷登録頭数）', round(d['予防注射頭数'][0] / d['登録頭数'][0] * 100, 1), '%', '計算',
            d['登録頭数'][1], '予防注射頭数÷登録頭数×100。昭和の年は注射頭数が登録頭数を上回る（未登録犬への注射等）')

rows.sort(key=lambda r: (r['動物'], r['年'] if r['年'] != '' else 0, r['項目']))
cols = ['年', '年度または暦年', '動物', '項目', '値', '単位', '区分', '出典URL', '取得日', '備考']
with open(f'{ROOT}/clean/狂犬病_登録注射.csv', 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
print('rows', len(rows))
print('検算 年, 厚労省登録, e-Stat登録, 厚労省注射, e-Stat注射')
for c in estat_check:
    flag = '' if c[1] == c[2] and c[3] == c[4] else '  <-- 不一致'
    print(*c, flag)
