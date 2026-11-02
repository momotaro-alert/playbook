"""Phase1: 犬・猫の引取り及び処分の状況（都道府県・指定都市・中核市）
出力:
  clean/引取り処分_都道府県別_自治体単位.csv  （原表の自治体単位, 実測）
  clean/引取り処分_都道府県別_県合算.csv      （指定都市・中核市を所在都道府県に合算, 計算）
usage: python3 -I work/phase1_takedown_pref.py
"""
import sys, os, re
from collections import defaultdict
sys.path.insert(0, '/home/user/playbook/pet-data/work')
from phase1_util import *

FILES = {  # データ年度: (raw path, 形式)
    2009: ('council/h22/900435039.pdf', 'f09'),
    2010: ('council/h23/900435078.pdf', 'single'),
    2011: ('council/h24/900435151.pdf', 'single'),
    2012: ('council/h25/900434840.pdf', 'single'),
    2013: ('h26/h26_3_4_3.pdf', 'single'),
    2014: ('h27/h27_3_4_3.pdf', 'single'),
    2015: ('h28/h28_3_4_3.pdf', 'tri6'),
    2016: ('h29/h29_3_4_3.pdf', 'tri6'),
    2017: ('h30/h30_3_4_3a.pdf', 'tri6'),
    2018: ('r01/r01_3_4_3a.pdf', 'tri12'),
    2019: ('r02/2_4_3a.pdf', 'tri12'),
    2020: ('r03/2_4_3a.pdf', 'tri12'),
    2021: ('r04/2_4_3a.pdf', 'tri12'),
    2022: ('r05/2_4_3a.pdf', 'tri12'),
    2023: ('r06/2_4_3a.pdf', 'tri12'),
    2024: ('r07/2_4_3a.pdf', 'tri12'),
}
D10 = ['引取り_飼い主から_成熟', '引取り_飼い主から_幼齢', '引取り_所有者不明_成熟', '引取り_所有者不明_幼齢',
       '返還数', '返還数_うち幼齢', '譲渡数', '譲渡数_うち幼齢', '殺処分数', '殺処分数_うち幼齢']
T4 = ['引取り数', '返還数', '譲渡数', '殺処分数']
MID6 = ['引取り_飼い主から_成熟', '引取り_飼い主から_幼齢', '引取り_所有者不明_成熟', '引取り_所有者不明_幼齢',
        '引取り_合計_成熟', '引取り_合計_幼齢']
TOP3 = ['返還数', '譲渡数', '殺処分数']
TOP6 = ['返還数', '譲渡数', '殺処分数_①', '殺処分数_②', '殺処分数_③', '殺処分数']

# pdftotext で文字が二重化（太字重ね打ち）して読めない行: pdfplumber の抽出文字列から重複文字を除いて目視で確定した値
FIX = {
    (2009, '滋賀県'): '644 232 363 513 226 1,187 66 1,347 2,289 429 1,860',
    (2009, '長崎市'): '207 26 184 77 278 2,559 167 2,670 3,070 351 2,747',
    # 原表で猫の所有者不明成熟が「*」(注:*飼主からの引取りに含む)、所有者不明幼齢が空欄 -> 欠測扱い
    (2010, '愛知県'): '324 40 1,279 499 510 0 535 317 1,097 222 499 2,608 - - 0 0 386 301 2,721 2,307 5,249 510 921 3,818',
    # 原表で犬の所有者不明幼齢が空欄 -> 欠測扱い
    (2022, '明石市'): '0 0 8 - 8 0 6 0 19 11 25 11 44 6 36 2',
}

COLS = ['年度または暦年', '年', '自治体名', '自治体区分', '都道府県', '動物', '項目', '値', '単位', '区分', '出典URL', '取得日', '備考']


def parse(fy, src, fmt):
    text = pdftext(os.path.join(RAW, src))
    recs = []  # (name, dict animal->item->val)
    pending = None
    last = None
    started = False
    for line in text.splitlines():
        if '負傷動物' in line and started:
            break
        name, nums = split_line(line)
        name = norm_name(name)
        if name and (pref_of(name) or re.search(r'(市|県|都|府|道)$', name)) and nums:
            started = True
            d = defaultdict(dict)
            junk = [t for t in nums if not is_num(t)]
            if junk:
                print('NOTE junk tokens', fy, name, junk)
            nums = [t for t in nums if is_num(t)]
            if (fy, name) in FIX:
                nums = FIX[(fy, name)].split()
            v = [to_val(t) for t in nums]
            ok = True
            if fmt == 'single':
                if len(v) != 24:
                    ok = False
                else:
                    for i, it in enumerate(D10):
                        d['犬'][it] = v[i]
                        d['猫'][it] = v[10 + i]
                    for i, it in enumerate(T4):
                        d['犬猫計'][it] = v[20 + i]
            elif fmt == 'f09':
                if len(v) != 11:
                    ok = False
                else:
                    for i, it in enumerate(['引取り_成熟', '引取り_幼齢', '返還・譲渡数', '殺処分数']):
                        d['犬'][it] = v[i]
                        d['猫'][it] = v[4 + i]
                    for i, it in enumerate(['引取り数', '返還・譲渡数', '殺処分数']):
                        d['犬猫計'][it] = v[8 + i]
            else:
                if len(v) != 16:
                    ok = False
                else:
                    for i, it in enumerate(MID6):
                        d['犬'][it] = v[i]
                        d['猫'][it] = v[6 + i]
                    for i, it in enumerate(T4):
                        d['犬猫計'][it] = v[12 + i]
                    top = TOP3 if fmt == 'tri6' else TOP6
                    k = len(top)
                    if pending is None or len(pending) != 2 * k:
                        print('WARN upper', fy, name, pending)
                    else:
                        for i, it in enumerate(top):
                            d['犬'][it] = pending[i]
                            d['猫'][it] = pending[k + i]
                pending = None
            if not ok:
                print('WARN count', fy, name, len(v), line.strip()[:120])
                continue
            recs.append([name, d])
            last = recs[-1]
            continue
        if not name and nums and fmt.startswith('tri'):
            vals = [to_val(t) for t in nums]
            k = 3 if fmt == 'tri6' else 6
            if last is not None and last[1].get('_lower') is None and len(vals) == 2 * k and pending is None and last[0] != '__done':
                # 直前の自治体の下段（幼齢内数）
                top = TOP3 if fmt == 'tri6' else TOP6
                for i, it in enumerate(top):
                    last[1]['犬'][it + '_うち幼齢'] = vals[i]
                    last[1]['猫'][it + '_うち幼齢'] = vals[k + i]
                last[1]['_lower'] = True
            else:
                pending = vals
    # 下段が欠落した自治体の確認
    if fmt.startswith('tri'):
        for n, d in recs:
            if not d.get('_lower'):
                print('WARN no lower', fy, n)
    return recs


def main():
    rows = []
    for fy, (src, fmt) in sorted(FILES.items()):
        url = meta_url(os.path.join(RAW, src))
        recs = parse(fy, src, fmt)
        names = [n for n, _ in recs]
        dup = {n for n in names if names.count(n) > 1}
        if dup:
            print('WARN dup', fy, dup)
        unk = [n for n in names if not pref_of(n)]
        print(fy, fmt, 'n=', len(recs), 'unknown:', unk)
        for n, d in recs:
            for a in ('犬', '猫', '犬猫計'):
                for it, v in d.get(a, {}).items():
                    rows.append({'年度または暦年': '年度', '年': fy, '自治体名': n, '自治体区分': kind_of(n),
                                 '都道府県': pref_of(n) or '', '動物': a, '項目': it, '値': '' if v is None else v,
                                 '単位': '頭', '区分': '実測', '出典URL': url, '取得日': TODAY,
                                 '備考': '原表「-」（未集計等）' if v is None else ''})
    write_csv(os.path.join(CLEAN, '引取り処分_都道府県別_自治体単位.csv'), rows, COLS)
    print('rows', len(rows))
    # 県合算
    agg = defaultdict(lambda: [0, 0, [], set()])
    for r in rows:
        p = r['都道府県']
        if not p:
            continue
        k = (r['年'], p, r['動物'], r['項目'])
        if r['値'] == '':
            agg[k][1] += 1
            agg[k][2].append(r['自治体名'])
        else:
            agg[k][0] += r['値']
        agg[k][3].add(r['自治体名'])
        agg[k].append(r['出典URL']) if False else None
    url_by_year = {fy: meta_url(os.path.join(RAW, s)) for fy, (s, _) in FILES.items()}
    out = []
    for (fy, p, a, it), (s, nmiss, miss, members) in sorted(agg.items()):
        note = f'構成自治体: {"・".join(sorted(members))}'
        if nmiss:
            note += f' ／ 「-」の自治体（合算から除外）: {"・".join(miss)}'
        out.append({'年度または暦年': '年度', '年': fy, '都道府県': p, '動物': a, '項目': it,
                    '値': '' if nmiss == len(members) else s, '単位': '頭', '区分': '計算',
                    '構成自治体数': len(members), '出典URL': url_by_year[fy], '取得日': TODAY, '備考': note})
    write_csv(os.path.join(CLEAN, '引取り処分_都道府県別_県合算.csv'), out,
              ['年度または暦年', '年', '都道府県', '動物', '項目', '値', '単位', '区分', '構成自治体数', '出典URL', '取得日', '備考'])
    print('agg rows', len(out))


if __name__ == '__main__':
    main()
