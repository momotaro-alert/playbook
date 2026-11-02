"""Phase1: 犬の登録頭数（厚労省 衛生行政報告例の環境省再掲）とマイクロチップ登録頭数
出力: clean/犬登録頭数_環境省再掲.csv, clean/マイクロチップ.csv
入力: r07/2_6.pdf（昭和35年〜令和6年度）, r06/2_6.pdf（照合用）, r07/2_7.pdf, r06/2_7_1.pdf, r07/2_7_1.pdf, r06/2_7_2.pdf
usage: python3 -I work/phase1_dog_mc.py
"""
import sys, os, re
sys.path.insert(0, '/home/user/playbook/pet-data/work')
from phase1_util import *

DOG_ITEMS = ['登録頭数', '予防注射頭数', '徘徊犬_抑留頭数', '徘徊犬_返還頭数', '徘徊犬_差引頭数']


def parse_dog(src):
    text = pdftext(os.path.join(RAW, src))
    era = None
    out = {}
    for line in text.splitlines():
        s = line.strip().translate(Z2H)
        m = re.match(r'^(昭和|平成|令和)?\s*(元|\d+)\s*(年度|年)?\s*((?:※\d)*)\s+([\d,\s]+)$', s)
        if not m:
            continue
        if m.group(1):
            era = m.group(1)
        if era is None:
            continue
        nums = m.group(5).split()
        if len(nums) != 5:
            continue
        n = 1 if m.group(2) == '元' else int(m.group(2))
        y = ERA[era] + n
        kind = '年度' if y >= 1997 else '暦年'
        out[y] = (kind, [to_val(t) for t in nums], m.group(4))
    return out


def dog():
    src = 'r07/2_6.pdf'
    url = meta_url(os.path.join(RAW, src))
    d = parse_dog(src)
    notes = {'※1': '昭和60年4月から予防注射期間が半年→1年に改正。予防注射頭数に旧制度(1〜3月)と新制度(4〜12月)を含む',
             '※2': '平成9年度から年度単位の集計',
             '※4': '東日本大震災の影響で岩手県陸前高田市・大槌町の1〜3月分、宮城県(仙台市以外)、福島県相双保健福祉事務所管内を含まない',
             '※5': '予防注射頭数は茨城県の修正連絡により衛生行政報告例の数値と異なる'}
    rows = []
    for y, (kind, vals, mk) in sorted(d.items()):
        note = ' / '.join(notes.get(x, x) for x in re.findall(r'※\d', mk))
        for it, v in zip(DOG_ITEMS, vals):
            n2 = note
            if it == '徘徊犬_返還頭数':
                n2 = (n2 + ' / ' if n2 else '') + '返還頭数=抑留後元の飼い主に返還された頭数'
            if it == '徘徊犬_差引頭数':
                n2 = (n2 + ' / ' if n2 else '') + '差引頭数には第三者へ譲渡された犬の頭数を含む'
            rows.append({'年度または暦年': kind, '年': y, '動物': '犬', '項目': it, '値': v, '単位': '頭', '区分': '二次',
                         '出典URL': url, '取得日': TODAY,
                         '備考': ('原典: 厚生労働省 衛生行政報告例（環境省 動物愛護管理行政事務提要 令和7年度版 2_6 に再掲）。' + n2).strip()})
    rows.append({'年度または暦年': '年度', '年': '', '動物': '猫', '項目': '登録頭数', '値': '', '単位': '頭', '区分': '',
                 '出典URL': url, '取得日': TODAY, '備考': '猫には制度がない（狂犬病予防法の登録・予防注射は犬のみ）'})
    write_csv(os.path.join(CLEAN, '犬登録頭数_環境省再掲.csv'), rows,
              ['年度または暦年', '年', '動物', '項目', '値', '単位', '区分', '出典URL', '取得日', '備考'])
    print('dog years', len(d), min(d), max(d))
    return d


def mc():
    rows = []
    # 全国累積
    for src in ['r07/2_7.pdf', 'r06/2_7_1.pdf']:
        url = meta_url(os.path.join(RAW, src))
        for line in pdftext(os.path.join(RAW, src)).splitlines():
            m = re.match(r'^\s*(令和\S+?)年度末\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s*$', line)
            if not m:
                continue
            y = era_year(m.group(1) + '年')
            for a, v in zip(['犬', '猫', '犬猫計'], m.groups()[1:]):
                rows.append({'年度または暦年': '年度', '年': y, '基準': f'{y}年度末（{y + 1}-03-31）時点 累積', '地域': '全国',
                             '動物': a, '項目': '登録頭数_累積（年度末）', '値': to_val(v), '単位': '頭', '区分': '実測',
                             '出典URL': url, '取得日': TODAY,
                             '備考': '指定登録機関DBの年度末累積。死亡等届出分を含まない' + ('。令和4年度は2022年6月1日施行以降の登録分' if y == 2022 else '')})
    # 都道府県
    for src, y in [('r07/2_7_1.pdf', 2024), ('r06/2_7_2.pdf', 2023)]:
        url = meta_url(os.path.join(RAW, src))
        n = 0
        for line in pdftext(os.path.join(RAW, src)).splitlines():
            name, nums = split_line(line)
            name = resolve_name(name)
            if not (name in PREFS or name in ('合計', '全国', '計')) or len(nums) != 3:
                continue
            for a, v in zip(['犬', '猫', '犬猫計'], nums):
                rows.append({'年度または暦年': '年度', '年': y, '基準': f'{y}年度末 累積', '地域': name, '動物': a,
                             '項目': '登録頭数_累積（年度末）', '値': to_val(v), '単位': '頭', '区分': '実測', '出典URL': url,
                             '取得日': TODAY, '備考': '都道府県別（指定都市等を含む都道府県単位）'})
            n += 1
        print('mc pref', y, n)
    # 年度別純増（計算）: 全国 r07 の累積差分
    nat = {(r['年'], r['動物']): r['値'] for r in rows if r['地域'] == '全国' and 'r07' in r['出典URL']}
    for (y, a), v in sorted(nat.items()):
        if (y - 1, a) in nat:
            rows.append({'年度または暦年': '年度', '年': y, '基準': f'{y}年度末累積 − {y - 1}年度末累積', '地域': '全国', '動物': a,
                         '項目': '登録頭数_年度純増（累積差）', '値': v - nat[(y - 1, a)], '単位': '頭', '区分': '計算',
                         '出典URL': BASE + 'files/r07/2_7.pdf', '取得日': TODAY,
                         '備考': '新規登録数ではない（死亡等届出による減少を差し引いた純増）'})
        elif y == 2022:
            rows.append({'年度または暦年': '年度', '年': y, '基準': '2022-06-01〜2023-03-31', '地域': '全国', '動物': a,
                         '項目': '登録頭数_年度純増（累積差）', '値': v, '単位': '頭', '区分': '計算',
                         '出典URL': BASE + 'files/r07/2_7.pdf', '取得日': TODAY,
                         '備考': '制度開始年度のため累積値＝期間中の純増'})
    write_csv(os.path.join(CLEAN, 'マイクロチップ.csv'), rows,
              ['年度または暦年', '年', '基準', '地域', '動物', '項目', '値', '単位', '区分', '出典URL', '取得日', '備考'])
    print('mc rows', len(rows))


if __name__ == '__main__':
    d7 = dog()
    d6 = parse_dog('r06/2_6.pdf')
    diff = [(y, d6[y][1], d7[y][1]) for y in d6 if y in d7 and d6[y][1] != d7[y][1]]
    print('r06 vs r07 dog diffs:', diff)
    mc()
