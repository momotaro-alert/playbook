"""Phase1 検算: clean/ の各CSVを読み、内訳和・合計の整合を全年度で確認する。
出力: clean/検算結果_phase1.csv  （不一致は logs/phase1.md に転記）
usage: python3 -I work/phase1_checks.py
"""
import sys, os
import pandas as pd
sys.path.insert(0, '/home/user/playbook/pet-data/work')
from phase1_util import *

R = []


def chk(name, year, target, lname, lval, rname, rval, note=''):
    ok = (pd.notna(lval) and pd.notna(rval) and int(lval) == int(rval))
    R.append({'検算名': name, '年': year, '対象': target, '左辺': lname, '左辺値': None if pd.isna(lval) else int(lval),
              '右辺': rname, '右辺値': None if pd.isna(rval) else int(rval),
              '差(左-右)': (int(lval) - int(rval)) if (pd.notna(lval) and pd.notna(rval)) else None,
              '判定': '一致' if ok else ('判定不能(欠測)' if (pd.isna(lval) or pd.isna(rval)) else '不一致'), '備考': note})


def rd(f):
    d = pd.read_csv(os.path.join(CLEAN, f))
    d['値'] = pd.to_numeric(d['値'], errors='coerce')
    return d


# ---------------- 1. 動物取扱業 のべ合計 = 各業種の和 ----------------
b = rd('動物取扱業_登録数_全国.csv')
I1 = ['第一種_販売', '第一種_保管', '第一種_貸出し', '第一種_訓練', '第一種_展示', '第一種_競りあっせん業', '第一種_譲受飼養業']
I2 = ['第二種_譲渡し', '第二種_保管', '第二種_貸出し', '第二種_訓練', '第二種_展示']
for d, g in b.groupby('基準日'):
    v = g.set_index('項目')['値']
    chk('取扱業(全国) 第一種のべ合計=各業種の和', d, '全国', '第一種_業種計(のべ数)', v.get('第一種_業種計(のべ数)'),
        '+'.join(I1), v.reindex(I1).fillna(0).sum())
    if pd.notna(v.get('第二種_業種計(のべ数)')):
        chk('取扱業(全国) 第二種のべ合計=各業種の和', d, '全国', '第二種_業種計(のべ数)', v.get('第二種_業種計(のべ数)'),
            '+'.join(I2), v.reindex(I2).fillna(0).sum())
    if pd.notna(v.get('第一種_販売のうち犬猫等販売業')):
        R.append({'検算名': '取扱業(全国) 内数関係 繁殖≦犬猫等販売≦販売', '年': d, '対象': '全国',
                  '左辺': '繁殖/犬猫等販売/販売', '左辺値': None, '右辺': '', '右辺値': None, '差(左-右)': None,
                  '判定': '一致' if v['第一種_犬猫等販売業のうち繁殖を行う者'] <= v['第一種_販売のうち犬猫等販売業'] <= v['第一種_販売'] else '不一致',
                  '備考': f"{int(v['第一種_犬猫等販売業のうち繁殖を行う者'])}/{int(v['第一種_販売のうち犬猫等販売業'])}/{int(v['第一種_販売'])}"})

# 都道府県別: 自治体の和 = 原表合計、原表合計 = 総括表、各自治体のべ計=業種和
p = rd('動物取扱業_登録数_都道府県別.csv')
pj = p[p['集計単位'] == '自治体']
for d, g in pj.groupby('基準日'):
    tot = g[g['自治体名'] == '合計'].set_index('項目')['値']
    s = g[g['自治体名'] != '合計'].groupby('項目')['値'].sum()
    nat = b[b['基準日'] == d].set_index('項目')['値']
    for it in tot.index:
        chk('取扱業(都道府県表) 自治体の和=原表合計', d, '全国', f'Σ自治体 {it}', s.get(it), f'原表合計 {it}', tot.get(it))
        if it in nat.index:
            chk('取扱業 都道府県表合計=総括表(R07版)', d, '全国', f'都道府県表合計 {it}', tot.get(it), f'総括表 {it}', nat.get(it),
                '都道府県表は各年度版、総括表は令和7年度版（後年修正の可能性）')
    for n, gg in g.groupby('自治体名'):
        v = gg.set_index('項目')['値']
        if '第一種_業種計(のべ数)' in v.index:
            rs = v.reindex(I1).fillna(0).sum()
            if int(rs) != int(v['第一種_業種計(のべ数)']):
                chk('取扱業(自治体) 第一種のべ計=業種和', d, n, '第一種_業種計(のべ数)', v['第一種_業種計(のべ数)'], '業種和', rs)
        if '第二種_業種計(のべ数)' in v.index:
            rs = v.reindex(I2).fillna(0).sum()
            if int(rs) != int(v['第二種_業種計(のべ数)']):
                chk('取扱業(自治体) 第二種のべ計=業種和', d, n, '第二種_業種計(のべ数)', v['第二種_業種計(のべ数)'], '業種和', rs)
    R.append({'検算名': '取扱業(自治体) のべ計=業種和（不一致のみ個別行）', '年': d, '対象': '全自治体', '左辺': '', '左辺値': None,
              '右辺': '', '右辺値': None, '差(左-右)': None, '判定': '実施', '備考': f'{g["自治体名"].nunique()}自治体を検査'})

# ---------------- 2. 引取り（全国） ----------------
n = rd('引取り処分_全国長期.csv')
det = n[n['系列'].str.startswith('各年度版')]
ref = n[n['系列'].str.startswith('参考表')]
lt = n[n['系列'].str.startswith('長期表')]
html = n[n['系列'].str.startswith('dog-cat')]
for y in sorted(det['年'].unique()):
    for a in ['犬', '猫']:
        v = det[(det['年'] == y) & (det['動物'] == a)].set_index('項目')['値']
        r = ref[(ref['年'] == y) & (ref['動物'] == a)].set_index('項目')['値']
        if '引取り_飼い主から_成熟' in v.index:
            seijuku = v['引取り_飼い主から_成熟'] + v['引取り_所有者不明_成熟']
            yorei = v['引取り_飼い主から_幼齢'] + v['引取り_所有者不明_幼齢']
            kainushi = v['引取り_飼い主から_成熟'] + v['引取り_飼い主から_幼齢']
            fumei = v['引取り_所有者不明_成熟'] + v['引取り_所有者不明_幼齢']
            chk('引取り(全国) 引取り合計=成熟+幼齢', y, a, '引取り数(参考表)', r.get('引取り数'), '成熟+幼齢(詳細表)', seijuku + yorei)
            chk('引取り(全国) 引取り合計=飼い主から+所有者不明', y, a, '引取り数(参考表)', r.get('引取り数'),
                '飼い主から+所有者不明(詳細表)', kainushi + fumei)
            chk('処分(全国) 返還+譲渡=返還・譲渡数(参考表)', y, a, '返還数+譲渡数', v['返還数'] + v['譲渡数'], '返還・譲渡数(参考表)',
                r.get('返還・譲渡数'))
            chk('処分(全国) 殺処分 詳細表=参考表', y, a, '殺処分数(詳細表)', v['殺処分数'], '殺処分数(参考表)', r.get('殺処分数'),
                '詳細表=当該年度版、参考表=令和7年度版')
            for it in ['返還数', '譲渡数', '殺処分数']:
                if v.get(it + '_うち幼齢', 0) > v.get(it, 0):
                    chk(f'処分(全国) {it}_うち幼齢≦{it}', y, a, it + '_うち幼齢', v[it + '_うち幼齢'], it, v[it])
        elif '引取り_成熟' in v.index:
            chk('引取り(全国) 引取り合計=成熟+幼齢', y, a, '引取り数(参考表)', r.get('引取り数'), '成熟+幼齢(詳細表)',
                v['引取り_成熟'] + v['引取り_幼齢'], '平成21年度は飼い主から/所有者不明の内訳なし')
            R.append({'検算名': '引取り(全国) 引取り合計=飼い主から+所有者不明', '年': y, '対象': a, '左辺': '', '左辺値': None,
                      '右辺': '', '右辺値': None, '差(左-右)': None, '判定': '判定不能(欠測)', '備考': '平成21年度表に内訳なし'})
    t = det[(det['年'] == y) & (det['動物'] == '犬猫計')].set_index('項目')['値']
    dsum = det[(det['年'] == y) & (det['動物'].isin(['犬', '猫']))]
    if '引取り数' in t.index:
        comp = dsum[dsum['項目'].str.match(r'^引取り_(飼い主から|所有者不明|成熟|幼齢)')]['値'].sum()
        chk('引取り(全国) 犬猫計=犬+猫', y, '犬猫計', '犬猫計 引取り数', t['引取り数'], '犬・猫の引取り内訳の和', comp)
        if '殺処分数' in t.index:
            chk('処分(全国) 犬猫計殺処分=犬+猫', y, '犬猫計', '犬猫計 殺処分数', t['殺処分数'], '犬+猫 殺処分数',
                dsum[dsum['項目'] == '殺処分数']['値'].sum())
# 参考表: 犬+猫=合計
for y in sorted(ref['年'].unique()):
    for it in ['引取り数', '返還・譲渡数', '殺処分数']:
        g = ref[(ref['年'] == y) & (ref['項目'] == it)].set_index('動物')['値']
        chk(f'参考表 犬+猫=合計 {it}', y, '犬猫計', f'合計 {it}', g.get('犬猫計'), f'犬+猫', g.get('犬', 0) + g.get('猫', 0))
# 長期表と参考表の重複年(2004,2005)
for y in (2004, 2005):
    for a in ['犬', '猫']:
        l = lt[(lt['年'] == y) & (lt['動物'] == a)].set_index('項目')['値']
        r = ref[(ref['年'] == y) & (ref['動物'] == a)].set_index('項目')['値']
        chk('長期表S49-H17 vs 参考表H16-R06 引取り数', y, a, '長期表 引取り数', l.get('引取り数'), '参考表 引取り数', r.get('引取り数'),
            '犬は参考表が狂犬病予防法の抑留を勘案した推計値のため不一致が想定される' if a == '犬' else '')
        chk('長期表S49-H17 vs 参考表H16-R06 殺処分数', y, a, '長期表 殺処分数', l.get('殺処分数'), '参考表 殺処分数', r.get('殺処分数'),
            '犬は系列定義が異なる' if a == '犬' else '')
# HTML(令和6年度) vs PDF
for a in ['犬', '猫']:
    h = html[(html['動物'] == a)].set_index('項目')['値']
    v = det[(det['年'] == 2024) & (det['動物'] == a)].set_index('項目')['値']
    chk('令和6年度 殺処分=①+②+③(HTML全国表)', 2024, a, '殺処分数(PDF)', v['殺処分数'], '①+②+③(HTML)',
        h['殺処分数_①'] + h['殺処分数_②'] + h['殺処分数_③'])
    chk('令和6年度 負傷動物 殺処分=①+②+③(HTML全国表)', 2024, a, '負傷動物_殺処分数(PDF)', v['負傷動物_殺処分数'], '①+②+③(HTML)',
        h['負傷動物_殺処分数_①'] + h['負傷動物_殺処分数_②'] + h['負傷動物_殺処分数_③'])

# dog-cat.html の参考表(平成16〜令和6年度) と PDF参考表の照合
from bs4 import BeautifulSoup
soup = BeautifulSoup(open(os.path.join(RAW, 'dog-cat.html'), 'rb').read(), 'html.parser')
for tr in soup.find_all('tr'):
    if tr.find('table'):
        continue
    c = [x.get_text(strip=True) for x in tr.find_all(['td', 'th'])]
    if len(c) == 10 and era_year(c[0]):
        y = era_year(c[0])
        vals = [int(x.replace(',', '')) for x in c[1:]]
        for (a, it), hv in zip([(a, it) for a in ['犬', '猫', '犬猫計'] for it in ['引取り数', '返還・譲渡数', '殺処分数']], vals):
            pv = ref[(ref['年'] == y) & (ref['動物'] == a) & (ref['項目'] == it)]['値']
            chk('参考表 PDF(R07版2_4_1)=HTML(dog-cat.html)', y, a, f'PDF {it}', pv.iloc[0] if len(pv) else None, f'HTML {it}', hv)

# ---------------- 3. 引取り（都道府県別） ----------------
pp = rd('引取り処分_都道府県別_自治体単位.csv')
for y in sorted(pp['年'].unique()):
    g = pp[pp['年'] == y]
    # 全国照合
    s = g.groupby(['動物', '項目'])['値'].sum()
    dd = det[det['年'] == y].set_index(['動物', '項目'])['値']
    nmatch = nmis = 0
    for k, val in s.items():
        if k in dd.index:
            if int(val) == int(dd[k]):
                nmatch += 1
            else:
                nmis += 1
                chk('都道府県表 Σ自治体=全国表', y, f'{k[0]}', f'Σ自治体 {k[1]}', val, f'全国表 {k[1]}', dd[k])
    R.append({'検算名': '都道府県表 Σ自治体=全国表（項目数）', '年': y, '対象': '全国', '左辺': '一致項目数', '左辺値': nmatch,
              '右辺': '不一致項目数', '右辺値': nmis, '差(左-右)': None, '判定': '一致' if nmis == 0 else '不一致', '備考': ''})
    # 自治体ごとの内訳検算（不一致のみ出力し、件数を集計）
    cnt = {'成熟幼齢': [0, 0], '殺処分①②③': [0, 0], '犬猫計': [0, 0]}
    for (nm, a), gg in g.groupby(['自治体名', '動物']):
        v = gg.set_index('項目')['値']
        if '引取り_合計_成熟' in v.index:
            for k in ('成熟', '幼齢'):
                lhs = v.get(f'引取り_合計_{k}')
                rhs = v.get(f'引取り_飼い主から_{k}', 0) + v.get(f'引取り_所有者不明_{k}', 0)
                if pd.notna(lhs) and pd.notna(rhs):
                    cnt['成熟幼齢'][0] += 1
                    if int(lhs) != int(rhs):
                        cnt['成熟幼齢'][1] += 1
                        chk('引取り(自治体) 合計_' + k + '=飼い主から+所有者不明', y, f'{nm}/{a}', f'引取り_合計_{k}', lhs,
                            '飼い主から+所有者不明', rhs)
        for suf in ('', '_うち幼齢'):
            if f'殺処分数_①{suf}' in v.index:
                lhs = v.get(f'殺処分数{suf}')
                parts = [v.get(f'殺処分数_{c}{suf}') for c in '①②③']
                if pd.notna(lhs) and all(pd.notna(x) for x in parts):
                    cnt['殺処分①②③'][0] += 1
                    if int(lhs) != int(sum(parts)):
                        cnt['殺処分①②③'][1] += 1
                        chk('殺処分(自治体) 殺処分=①+②+③' + suf, y, f'{nm}/{a}', '殺処分数' + suf, lhs, '①+②+③', sum(parts))
    for (nm), gg in g.groupby('自治体名'):
        t = gg[gg['動物'] == '犬猫計'].set_index('項目')['値']
        for it in ['返還数', '譲渡数', '殺処分数']:
            if it in t.index:
                rhs = gg[(gg['動物'].isin(['犬', '猫'])) & (gg['項目'] == it)]['値']
                if t[it] == t[it] and rhs.notna().all():
                    cnt['犬猫計'][0] += 1
                    if int(t[it]) != int(rhs.sum()):
                        cnt['犬猫計'][1] += 1
                        chk('処分(自治体) 犬猫計=犬+猫', y, nm, f'犬猫計 {it}', t[it], '犬+猫', rhs.sum())
    for k, (a, m) in cnt.items():
        R.append({'検算名': f'自治体内訳検算 {k}（件数集計）', '年': y, '対象': '全自治体', '左辺': '検査件数', '左辺値': a,
                  '右辺': '不一致件数', '右辺値': m, '差(左-右)': None, '判定': ('該当なし' if a == 0 else ('一致' if m == 0 else '不一致あり')),
                  '備考': ''})

# 殺処分分類 全国(計算)=①+②+③
kc = rd('殺処分分類_全国.csv')
kcc = kc[kc['区分'] == '計算']
for (y, a), g in kcc.groupby(['年', '動物']):
    v = g.set_index('項目')['値']
    chk('殺処分(全国) 殺処分=①+②+③', y, a, '殺処分数(Σ自治体)', v.get('殺処分数'), '①+②+③(Σ自治体)',
        v.get('殺処分数_①') + v.get('殺処分数_②') + v.get('殺処分数_③'))
    if a in ('犬', '猫'):
        r = ref[(ref['年'] == y) & (ref['動物'] == a)].set_index('項目')['値']
        chk('殺処分(全国) Σ自治体=参考表', y, a, '殺処分数(Σ自治体)', v.get('殺処分数'), '殺処分数(参考表R07版)', r.get('殺処分数'))
hh = kc[kc['区分'] == '実測']
for a in ['犬', '猫']:
    for c in '①②③':
        chk('令和6年度 ①②③ Σ自治体(計算)=HTML全国表(実測)', 2024, a, f'Σ自治体 殺処分数_{c}',
            kcc[(kcc['年'] == 2024) & (kcc['動物'] == a) & (kcc['項目'] == f'殺処分数_{c}')]['値'].sum(),
            f'HTML 殺処分数_{c}', hh[(hh['動物'] == a) & (hh['項目'] == f'殺処分数_{c}')]['値'].sum())

# ---------------- 4. 行政処分 ----------------
e = rd('行政処分_立入検査.csv')
for y in sorted(e['年'].unique()):
    g = e[(e['年'] == y)]
    tot = g[g['自治体名'] == '全国計'].groupby('項目')['値'].sum(min_count=1)
    s = g[g['集計単位'] == '自治体'].groupby('項目')['値'].sum(min_count=1)
    if s.empty:
        continue
    for it in ['第一種_立入検査件数(法24条1項)', '第一種_立入検査施設数(法24条1項)', '第一種_勧告(法23条1・2項)',
               '第一種_登録取消命令(法19条)', '第一種_業務停止命令(法19条)', '第二種_立入検査件数(法24条1項準用)']:
        if it in tot.index:
            chk('行政処分 Σ自治体=原表合計', y, '全国', f'Σ自治体 {it}', s.get(it), f'原表合計 {it}', tot.get(it),
                '東京都等「延べ件数のみ」注記の自治体が合計に含まれない年がある' if it.startswith('第一種_立入') else '')

# ---------------- 5. マイクロチップ ----------------
m = rd('マイクロチップ.csv')
for y in (2023, 2024):
    for a in ['犬', '猫', '犬猫計']:
        s = m[(m['年'] == y) & (m['動物'] == a) & (m['地域'] != '全国') & (m['項目'] == '登録頭数_累積（年度末）')]['値'].sum()
        nt = m[(m['年'] == y) & (m['動物'] == a) & (m['地域'] == '全国') & (m['項目'] == '登録頭数_累積（年度末）')]['値'].iloc[0]
        chk('マイクロチップ Σ都道府県=全国', y, a, 'Σ都道府県', s, '全国', nt)
for y in (2022, 2023, 2024):
    g = m[(m['年'] == y) & (m['地域'] == '全国') & (m['項目'] == '登録頭数_累積（年度末）') & m['出典URL'].str.contains('r07')]
    v = g.set_index('動物')['値']
    chk('マイクロチップ 犬+猫=合計', y, '全国', '合計', v['犬猫計'], '犬+猫', v['犬'] + v['猫'])
# r06版 と r07版の一致
for y in (2022, 2023):
    for a in ['犬', '猫', '犬猫計']:
        g = m[(m['年'] == y) & (m['地域'] == '全国') & (m['動物'] == a) & (m['項目'] == '登録頭数_累積（年度末）')]
        v6 = g[g['出典URL'].str.contains('r06')]['値'].iloc[0]
        v7 = g[g['出典URL'].str.contains('r07')]['値'].iloc[0]
        chk('マイクロチップ R06版=R07版', y, a, 'R06版', v6, 'R07版', v7)

out = pd.DataFrame(R)
out.insert(0, '年度または暦年', out['年'].map(lambda v: '暦年（基準日時点）' if '-' in str(v) else '年度'))
out['単位'] = '頭/事業所/件（各検算の対象に同じ）'
out['区分'] = '計算'
out['出典URL'] = 'clean/ 内の各CSV（各値の出典URLは元CSV参照）'
out['取得日'] = TODAY
out.to_csv(os.path.join(CLEAN, '検算結果_phase1.csv'), index=False, encoding='utf-8-sig')
print(out['判定'].value_counts().to_string())
bad = out[out['判定'].isin(['不一致', '不一致あり'])]
pd.set_option('display.width', 250)
print(bad[['検算名', '年', '対象', '左辺値', '右辺値', '差(左-右)']].to_string())
