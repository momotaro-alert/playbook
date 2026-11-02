"""Phase1: 動物取扱業の登録・届出数
出力:
  clean/動物取扱業_登録数_全国.csv      （r07/2_1_1 総括表：平成18年3月31日届出〜令和7年4月1日登録）
  clean/動物取扱業_登録数_都道府県別.csv （各年度版 都道府県・指定都市表 2010〜2025年4月1日。自治体単位＋県合算）
usage: python3 -I work/phase1_business.py
"""
import sys, os, re
from collections import defaultdict
import pdfplumber
sys.path.insert(0, '/home/user/playbook/pet-data/work')
from phase1_util import *

ITEMS18 = ['第一種_総事業所数(実数)', '第一種_販売', '第一種_販売のうち犬猫等販売業', '第一種_犬猫等販売業のうち繁殖を行う者',
           '第一種_保管', '第一種_貸出し', '第一種_訓練', '第一種_展示', '第一種_競りあっせん業', '第一種_譲受飼養業',
           '第一種_業種計(のべ数)', '第二種_総事業所数(実数)', '第二種_譲渡し', '第二種_保管', '第二種_貸出し',
           '第二種_訓練', '第二種_展示', '第二種_業種計(のべ数)']
# r07/2_1_1 の数値右端 x 座標 -> 列
XCOL = [220, 252, 285, 317, 349, 377, 406, 434, 461, 488, 521, 563, 592, 619, 646, 673, 700, 733]
COLS = ['年度または暦年', '年', '基準日', '制度', '項目', '値', '単位', '区分', '出典URL', '取得日', '備考']


def date_of(s):
    s = s.translate(Z2H)
    m = re.search(r'(平成|令和)(元|\d+)年(\d+)月(\d+)日', s)
    if not m:
        return None
    y = era_year(m.group(1) + m.group(2))
    return f'{y}-{int(m.group(3)):02d}-{int(m.group(4)):02d}'


def national():
    src = 'r07/2_1_1.pdf'
    url = meta_url(os.path.join(RAW, src))
    rows = []
    with pdfplumber.open(os.path.join(RAW, src)) as pdf:
        ws = pdf.pages[0].extract_words(x_tolerance=1.5)
    labels = [(w['top'], date_of(w['text'])) for w in ws if date_of(w['text'])]
    lines = defaultdict(list)
    for w in ws:
        if is_num(w['text']) and w['top'] > 130 and w['x0'] > 180:
            lines[round(w['top'])].append(w)
    for top, wl in sorted(lines.items()):
        lab = min(labels, key=lambda l: abs(l[0] - top))
        if abs(lab[0] - top) > 14:
            print('WARN no label', top, [w['text'] for w in wl])
            continue
        d = lab[1]
        seido = '届出制（旧法）' if d == '2006-03-31' else '登録制（第一種）・届出制（第二種）'
        for w in wl:
            j = min(range(len(XCOL)), key=lambda i: abs(XCOL[i] - w['x1']))
            assert abs(XCOL[j] - w['x1']) < 6, (d, w)
            it = ITEMS18[j]
            note = ''
            if d == '2006-03-31':
                note = '改正法施行(2006年6月)前の届出状況。項目名は第一種に読み替えて格納（当時は「動物取扱業」）'
            elif d < '2013-09-01':
                note = '当時は「動物取扱業」（第一種/第二種の区分なし）'
            rows.append({'年度または暦年': '暦年（基準日時点）', '年': int(d[:4]), '基準日': d, '制度': seido, '項目': it,
                         '値': to_val(w['text']), '単位': '事業所（業種は のべ）', '区分': '実測', '出典URL': url,
                         '取得日': TODAY, '備考': note})
    # 2014年以前に存在しない項目の注記行
    dates = sorted({r['基準日'] for r in rows})
    have = {(r['基準日'], r['項目']) for r in rows}
    for d in dates:
        for it in ITEMS18:
            if (d, it) not in have:
                rows.append({'年度または暦年': '暦年（基準日時点）', '年': int(d[:4]), '基準日': d, '制度': '', '項目': it,
                             '値': '', '単位': '事業所（業種は のべ）', '区分': '実測', '出典URL': url, '取得日': TODAY,
                             '備考': '当該時点では区分なし（第二種・犬猫等販売業・繁殖を行う者は2013年9月1日改正法施行で追加）'})
    rows.sort(key=lambda r: (r['基準日'], ITEMS18.index(r['項目'])))
    write_csv(os.path.join(CLEAN, '動物取扱業_登録数_全国.csv'), rows, COLS)
    print('national rows', len(rows), 'dates', dates)


PREF_FILES = {  # 基準日: (path, 形式)
    '2010-04-01': ('council/h22/900435032.pdf', 7),
    '2011-04-01': ('council/h23/900435071.pdf', 7),
    '2012-04-01': ('council/h24/900435144.pdf', 7),
    '2013-04-01': ('council/h25/900434831.pdf', 9),
    '2014-04-01': ('h26/h26_3_1_2.pdf', 18), '2015-04-01': ('h27/h27_3_1_2.pdf', 18),
    '2016-04-01': ('h28/h28_3_1_2.pdf', 18), '2017-04-01': ('h29/h29_3_1_2.pdf', 18),
    '2018-04-01': ('h30/h30_3_1_2.pdf', 18), '2019-04-01': ('r01/r01_3_1_2.pdf', 18),
    '2020-04-01': ('r02/2_1_2.pdf', 18), '2021-04-01': ('r03/2_1_2.pdf', 18),
    '2022-04-01': ('r04/2_1_2.pdf', 18), '2023-04-01': ('r05/2_1_2.pdf', 18),
    '2024-04-01': ('r06/2_1_2.pdf', 18), '2025-04-01': ('r07/2_1_2.pdf', 18),
}
I7 = ['第一種_総事業所数(実数)', '第一種_販売', '第一種_保管', '第一種_貸出し', '第一種_訓練', '第一種_展示', '第一種_業種計(のべ数)']
I9 = I7[:-1] + ['第一種_競りあっせん業', '第一種_譲受飼養業', '第一種_業種計(のべ数)']


def prefecture():
    rows = []
    for d, (src, k) in sorted(PREF_FILES.items()):
        url = meta_url(os.path.join(RAW, src))
        items = {7: I7, 9: I9, 18: ITEMS18}[k]
        text = pdftext(os.path.join(RAW, src))
        # 総括表と同居しているファイルは「都道府県」見出し以降のみ
        started = False
        seen = set()
        for line in text.splitlines():
            if re.search(r'都道府県|都道府', line):
                started = True
            if not started:
                continue
            name, nums = split_line(line)
            name = resolve_name(name)
            if name == '合計':
                pass
            elif not pref_of(name):
                continue
            nums = [t for t in nums if is_num(t)]
            if len(nums) != k:
                if nums:
                    print('WARN', d, name, len(nums), line.strip()[:100])
                continue
            if name in seen:
                continue
            seen.add(name)
            for it, t in zip(items, nums):
                rows.append({'年度または暦年': '暦年（基準日時点）', '年': int(d[:4]), '基準日': d, '集計単位': '自治体',
                             '自治体名': name, '自治体区分': '全国計' if name == '合計' else kind_of(name),
                             '都道府県': '全国' if name == '合計' else pref_of(name), '項目': it,
                             '値': to_val(t), '単位': '事業所（業種は のべ）', '区分': '実測', '出典URL': url,
                             '取得日': TODAY, '備考': '都道府県の数値には管下の指定都市分を含まない（原表注）' if name in PREFS else ''})
        print(d, 'jurisdictions', len(seen))
    # 県合算（指定都市を県に合算）
    agg = defaultdict(lambda: [0, set(), ''])
    for r in rows:
        if r['自治体名'] == '合計' or r['値'] is None:
            continue
        a = agg[(r['基準日'], r['都道府県'], r['項目'])]
        a[0] += r['値']
        a[1].add(r['自治体名'])
        a[2] = r['出典URL']
    for (d, p, it), (v, mem, url) in sorted(agg.items()):
        rows.append({'年度または暦年': '暦年（基準日時点）', '年': int(d[:4]), '基準日': d, '集計単位': '県合算',
                     '自治体名': p, '自治体区分': '都道府県（指定都市合算）', '都道府県': p, '項目': it, '値': v,
                     '単位': '事業所（業種は のべ）', '区分': '計算', '出典URL': url, '取得日': TODAY,
                     '備考': '構成: ' + '・'.join(sorted(mem))})
    write_csv(os.path.join(CLEAN, '動物取扱業_登録数_都道府県別.csv'), rows,
              ['年度または暦年', '年', '基準日', '集計単位', '自治体名', '自治体区分', '都道府県', '項目', '値', '単位', '区分',
               '出典URL', '取得日', '備考'])
    print('pref rows', len(rows))


if __name__ == '__main__':
    national()
    prefecture()
