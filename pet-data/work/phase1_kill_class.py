"""Phase1: 殺処分数の分類①②③（全国）
 ① 譲渡することが適切ではない（治療の見込みがない病気や攻撃性がある等）
 ② ①以外の殺処分
 ③ 引取り後の死亡
全国値は各年度版の都道府県別表(2_4_3a)の自治体値の合計（区分=計算）。令和6年度は dog-cat.html の全国表（実測）も併記。
分類集計は令和元年度版事務提要(=平成30年度データ)の都道府県表から存在するため 2018 年度も出力する。
入力: clean/引取り処分_都道府県別_自治体単位.csv, clean/引取り処分_全国長期.csv
出力: clean/殺処分分類_全国.csv
usage: python3 -I work/phase1_kill_class.py
"""
import sys, os
import pandas as pd
sys.path.insert(0, '/home/user/playbook/pet-data/work')
from phase1_util import *

p = pd.read_csv(os.path.join(CLEAN, '引取り処分_都道府県別_自治体単位.csv'))
n = pd.read_csv(os.path.join(CLEAN, '引取り処分_全国長期.csv'))
p['値'] = pd.to_numeric(p['値'])
items = ['殺処分数_①', '殺処分数_②', '殺処分数_③', '殺処分数']
rows = []
sub = p[p['項目'].isin(items + [i + '_うち幼齢' for i in items]) & p['動物'].isin(['犬', '猫']) & (p['年'] >= 2018)]
for (y, a, it), g in sub.groupby(['年', '動物', '項目']):
    miss = g['値'].isna().sum()
    rows.append({'年度または暦年': '年度', '年': y, '動物': a, '項目': it, '値': int(g['値'].sum()), '単位': '頭',
                 '区分': '計算', '出典URL': g['出典URL'].iloc[0], '取得日': TODAY,
                 '備考': f'都道府県・指定都市・中核市 {len(g)}自治体の合計' + (f'（「-」{miss}自治体を除く）' if miss else '')})
# 犬猫計
df = pd.DataFrame(rows)
for (y, it), g in df.groupby(['年', '項目']):
    rows.append({'年度または暦年': '年度', '年': y, '動物': '犬猫計', '項目': it, '値': int(g['値'].sum()), '単位': '頭',
                 '区分': '計算', '出典URL': g['出典URL'].iloc[0], '取得日': TODAY, '備考': '犬＋猫'})
# 実測（HTML 令和6年度）
h = n[n['系列'].str.startswith('dog-cat.html') & n['項目'].str.contains('①|②|③')]
for _, r in h.iterrows():
    rows.append({'年度または暦年': '年度', '年': r['年'], '動物': r['動物'], '項目': r['項目'], '値': r['値'], '単位': '頭',
                 '区分': '実測', '出典URL': r['出典URL'], '取得日': TODAY,
                 '備考': '環境省 dog-cat.html 全国表（負傷動物分は「負傷動物_」）'})
out = pd.DataFrame(rows).sort_values(['年', '動物', '区分', '項目'])
out.insert(len(out.columns) - 1, '分類定義', out['項目'].map(lambda s: '①譲渡することが適切ではない（治療の見込みがない病気・攻撃性等）' if '①' in s else
                                                       ('②①以外の殺処分' if '②' in s else ('③引取り後の死亡' if '③' in s else '①＋②＋③'))))
out.to_csv(os.path.join(CLEAN, '殺処分分類_全国.csv'), index=False, encoding='utf-8-sig')
print(out[(out['項目'].isin(items))].pivot_table(index=['年', '動物'], columns=['項目', '区分'], values='値').to_string())
