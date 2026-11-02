"""Phase1: 犬・猫の引取り及び処分（全国）
出力:
  clean/引取り処分_全国長期.csv  (ロング形式, 1974〜2024年度)
入力:
  r07/2_4_2.pdf      昭和49〜平成17年度 長期表（犬の引取りは抑留を含まない系列）
  r07/2_4_1.pdf      (参考)平成16〜令和6年度 犬猫別 引取り/返還・譲渡/殺処分 + 負傷込み
  各年度版 2_4_1 (全国統計) の当該年度詳細行: FY2009(H22版)〜FY2024(R07版)
usage: python3 -I work/phase1_takedown_national.py
"""
import sys, os, re
sys.path.insert(0, '/home/user/playbook/pet-data/work')
from phase1_util import *

OUT = os.path.join(CLEAN, '引取り処分_全国長期.csv')
COLS = ['年度または暦年', '年', '動物', '項目', '値', '単位', '区分', '系列', '出典表', '出典URL', '取得日', '備考']

# 各年度版の全国統計PDF  (データ年度 -> rawパス)
NATIONAL_DETAIL = {
    2009: 'council/h22/900435038.pdf',
    2010: 'council/h23/900435077.pdf',
    2011: 'council/h24/900435150.pdf',
    2012: 'council/h25/900434838.pdf',
    2013: 'h26/h26_3_4_1.pdf', 2014: 'h27/h27_3_4_1.pdf', 2015: 'h28/h28_3_4_1.pdf',
    2016: 'h29/h29_3_4_1.pdf', 2017: 'h30/h30_3_4_1.pdf', 2018: 'r01/r01_3_4_1.pdf',
    2019: 'r02/2_4_1.pdf', 2020: 'r03/2_4_1.pdf', 2021: 'r04/2_4_1.pdf', 2022: 'r05/2_4_1.pdf',
    2023: 'r06/2_4_1.pdf', 2024: 'r07/2_4_1.pdf',
}

rows = []


def add(year, animal, item, val, src, table, series, note='', kubun='実測'):
    rows.append({'年度または暦年': '年度', '年': year, '動物': animal, '項目': item,
                 '値': '' if val is None else val, '単位': '頭', '区分': kubun, '系列': series,
                 '出典表': table, '出典URL': meta_url(os.path.join(RAW, src)), '取得日': TODAY,
                 '備考': note if val is not None else (note + ' 表中「-」').strip()})


def year_lines(text):
    """年度ラベルで始まる行 -> list of (year, tokens)"""
    out = []
    for line in text.splitlines():
        s = line.strip()
        m = re.match(r'^((?:昭和|平成|令和)\s*(?:元|[0-9０-９]+)\s*年度?)(.*)$', s)
        if not m:
            continue
        y = era_year(m.group(1))
        toks = [t for t in m.group(2).split() if t != '(参考)']
        out.append((y, toks, s))
    return out


# ---------- 1) 昭和49〜平成17年度 長期表 ----------
src = 'r07/2_4_2.pdf'
tbl = '2_4_2 犬・猫の引取り及び負傷動物等の収容並びに処分の状況（全国：昭和49年度～平成17年度）'
ser = '長期表S49-H17（犬の引取りは狂犬病予防法の抑留を含まない）'
LT_ITEMS = [('犬', '引取り数'), ('犬', '譲渡数_一般'), ('犬', '譲渡数_その他'), ('犬', '殺処分数'),
            ('猫', '引取り数'), ('猫', '譲渡数_一般'), ('猫', '譲渡数_その他'), ('猫', '殺処分数'),
            ('犬', '負傷動物_収容数'), ('犬', '負傷動物_返還数'), ('猫', '負傷動物_収容数'), ('猫', '負傷動物_返還数'),
            ('その他', '負傷動物_収容数')]
n_lt = 0
for y, toks, s in year_lines(pdftext(os.path.join(RAW, src))):
    nums = [t for t in toks if is_num(t)]
    if len(nums) != 13:
        print('WARN longterm', y, len(nums), s)
        continue
    for (a, it), t in zip(LT_ITEMS, nums):
        note = '犬の処分数には狂犬病予防法に基づく抑留犬の処分数の一部が含まれる' if (a == '犬' and it == '殺処分数') else ''
        add(y, a, it, to_val(t), src, tbl, ser, note)
    n_lt += 1
print('longterm years', n_lt)

# ---------- 2) 参考表 平成16〜令和6年度 ----------
src = 'r07/2_4_1.pdf'
tbl = '2_4_1 (参考)平成16～令和6年度'
ser = '参考表H16-R06（H16/17の犬引取りは抑留を勘案した推計値）'
REF_ITEMS = [('犬', '引取り数'), ('犬', '返還・譲渡数'), ('犬', '殺処分数'),
             ('猫', '引取り数'), ('猫', '返還・譲渡数'), ('猫', '殺処分数'),
             ('犬猫計', '引取り数'), ('犬猫計', '返還・譲渡数'), ('犬猫計', '殺処分数')]
INJ_ITEMS = [('犬猫計', '負傷動物込み_収容数'), ('犬猫計', '負傷動物込み_返還・譲渡数'), ('犬猫計', '負傷動物込み_殺処分数')]
n_ref = 0
for y, toks, s in year_lines(pdftext(os.path.join(RAW, src))):
    if not re.search(r'\d+\.\d%', s):
        continue
    nums = [t for t in toks if is_num(t)]
    rate = re.search(r'(\d+\.\d)%', s).group(1)
    if len(nums) != 12:
        print('WARN ref', y, len(nums), s)
        continue
    for (a, it), t in zip(REF_ITEMS + INJ_ITEMS, nums):
        note = ''
        kub = '実測'
        if a == '犬' and it == '引取り数' and y in (2004, 2005):
            note = '狂犬病予防法に基づく抑留を勘案した推計値（原表注）'
            kub = '推測'
        if (y, a, it) == (2012, '猫', '殺処分数'):
            note = ('原PDF(R07版2_4_1)の値は123,220だが、同行の合計161,847・dog-cat.html・H25年度版全国統計はいずれも123,400。'
                    'PDFの誤記の可能性（値は原PDFのまま、詳細系列の123,400を参照）')
        add(y, a, it, to_val(t), src, tbl, ser, note, kubun=kub)
    rows.append({'年度または暦年': '年度', '年': y, '動物': '犬猫計', '項目': '殺処分率（原表）', '値': rate,
                 '単位': '%', '区分': '実測', '系列': ser, '出典表': tbl,
                 '出典URL': meta_url(os.path.join(RAW, src)), '取得日': TODAY, '備考': '原表記載の率'})
    n_ref += 1
print('ref years', n_ref)

# ---------- 3) 各年度版 全国統計 詳細 ----------
D10 = ['引取り_飼い主から_成熟', '引取り_飼い主から_幼齢', '引取り_所有者不明_成熟', '引取り_所有者不明_幼齢',
       '返還数', '返還数_うち幼齢', '譲渡数', '譲渡数_うち幼齢', '殺処分数', '殺処分数_うち幼齢']
T4 = ['引取り数', '返還数', '譲渡数', '殺処分数']
I7 = ['負傷動物_収容数', '負傷動物_返還数', '負傷動物_返還数_うち幼齢', '負傷動物_譲渡数', '負傷動物_譲渡数_うち幼齢',
      '負傷動物_殺処分数', '負傷動物_殺処分数_うち幼齢']
for fy, src in sorted(NATIONAL_DETAIL.items()):
    path = os.path.join(RAW, src)
    tbl = f'{os.path.basename(src)} 犬・猫の引取り及び負傷動物等の収容（並びに処分）の状況（全国）{fy}年度'
    ser = '各年度版 全国統計（当該年度）'
    yl = [(y, [t for t in toks if is_num(t)], s) for y, toks, s in year_lines(pdftext(path)) if y == fy]
    if fy == 2009:
        nums = yl[0][1]
        assert len(nums) == 17, nums
        items = [('犬', '引取り_成熟'), ('犬', '引取り_幼齢'), ('犬', '返還・譲渡数'), ('犬', '殺処分数'),
                 ('猫', '引取り_成熟'), ('猫', '引取り_幼齢'), ('猫', '返還・譲渡数'), ('猫', '殺処分数'),
                 ('犬猫計', '引取り数'), ('犬猫計', '返還・譲渡数'), ('犬猫計', '殺処分数'),
                 ('犬', '負傷動物_収容数'), ('犬', '負傷動物_返還・譲渡数'), ('犬', '負傷動物_殺処分数'),
                 ('猫', '負傷動物_収容数'), ('猫', '負傷動物_返還・譲渡数'), ('猫', '負傷動物_殺処分数')]
        for (a, it), t in zip(items, nums):
            add(fy, a, it, to_val(t), src, tbl, ser, '平成21年度は飼い主から/所有者不明の内訳なし')
        continue
    main = [x for x in yl if len(x[1]) == 24]
    inj = [x for x in yl if len(x[1]) == 14]
    if not main or not inj:
        print('WARN detail', fy, [(len(x[1]), x[2][:80]) for x in yl])
        continue
    nums = main[0][1]
    for i, it in enumerate(D10):
        add(fy, '犬', it, to_val(nums[i]), src, tbl, ser)
        add(fy, '猫', it, to_val(nums[10 + i]), src, tbl, ser)
    for i, it in enumerate(T4):
        add(fy, '犬猫計', it, to_val(nums[20 + i]), src, tbl, ser)
    nums = inj[0][1]
    for i, it in enumerate(I7):
        add(fy, '犬', it, to_val(nums[i]), src, tbl, ser)
        add(fy, '猫', it, to_val(nums[7 + i]), src, tbl, ser)
    print('detail', fy, 'ok')

# ---------- 4) 令和6年度 殺処分①②③（dog-cat.html の表；PDF には①②③が無い） ----------
import pandas as pd  # noqa
from bs4 import BeautifulSoup
hp = os.path.join(RAW, 'dog-cat.html')
soup = BeautifulSoup(open(hp, 'rb').read(), 'html.parser')
tabs = soup.find_all('table')
hurl = BASE + 'dog-cat.html'
for t in [soup]:
    for tr in t.find_all('tr'):
        if tr.find('table'):
            continue
        cells = [c.get_text(strip=True) for c in tr.find_all(['td', 'th'])]
        if not cells or cells[0] not in ('犬', '猫', '犬負傷', '猫負傷'):
            continue
        vals = [int(c.replace(',', '')) for c in cells[1:] if re.fullmatch(r'[\d,]+', c)]
        a = cells[0][0]
        if cells[0] in ('犬', '猫') and len(vals) == 14:
            names = ['引取り_飼い主から_成熟', '引取り_飼い主から_幼齢', '引取り_所有者不明_成熟', '引取り_所有者不明_幼齢',
                     '引取り数', '返還数', '返還数_うち幼齢', '譲渡数', '譲渡数_うち幼齢',
                     '殺処分数_①', '殺処分数_②', '殺処分数_③', '殺処分数', '殺処分数_うち幼齢']
        elif cells[0] in ('犬負傷', '猫負傷') and len(vals) == 10:
            names = ['負傷動物_収容数', '負傷動物_返還数', '負傷動物_返還数_うち幼齢', '負傷動物_譲渡数',
                     '負傷動物_譲渡数_うち幼齢', '負傷動物_殺処分数_①', '負傷動物_殺処分数_②', '負傷動物_殺処分数_③',
                     '負傷動物_殺処分数', '負傷動物_殺処分数_うち幼齢']
        else:
            continue
        for n, v in zip(names, vals):
            if '①' in n or '②' in n or '③' in n or n == '引取り数':
                rows.append({'年度または暦年': '年度', '年': 2024, '動物': a, '項目': n, '値': v, '単位': '頭',
                             '区分': '実測', '系列': 'dog-cat.html（令和6年度）',
                             '出典表': '環境省 統計資料「犬・猫の引取り及び負傷動物等の収容並びに処分の状況」HTML表',
                             '出典URL': hurl, '取得日': TODAY, '備考': ''})

seen = set()
out = []
for r in rows:
    k = (r['年'], r['動物'], r['項目'], r['系列'])
    if k in seen:
        continue
    seen.add(k)
    out.append(r)
out.sort(key=lambda r: (r['系列'], r['年'], r['動物'], r['項目']))
write_csv(OUT, out, COLS)
print('wrote', OUT, len(out))
