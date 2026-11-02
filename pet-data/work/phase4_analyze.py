#!/usr/bin/env python3
"""Phase 4 分析: raw/prices/petmi_listings.jsonl → clean/ の3ファイル

  python3 -I work/phase4_analyze.py

出力（UTF-8 BOM）:
  clean/店頭価格_明細.csv      1行=1掲載個体（散布図用: 生後日数 × 価格）
  clean/店頭価格_中央値表.csv   品種×生後日数ビン別の中央値、生後60日→365日下落率、掲載件数
  clean/店頭価格_チェーン別.csv チェーン×犬/猫（および×品種）の中央値

定義:
  生後日数 = 取得日 − 生年月日（日）
  ビン: 60日=45〜75日, 90日=75〜105日(75は含まない), 120日=105〜135日(105は含まない),
        180日=165〜195日, 365日=330〜400日（いずれも両端含む、ただし上記の重複境界は下位ビン優先）
  下落率(%) = (中央値60日 − 中央値365日) / 中央値60日 × 100。両ビンとも件数5以上の時のみ計算。
  価格は掲載表示の税込価格（ペットミー一覧は全件「税込」表示）。
  チェーン名は店舗名の文字列マッチによる推定（区分=推測）。
"""
import json, os, re
import pandas as pd

ROOT = '/home/user/playbook/pet-data'
SRC = os.path.join(ROOT, 'raw', 'prices', 'petmi_listings.jsonl')
CLEAN = os.path.join(ROOT, 'clean')

BINS = [  # (ラベル, 下限, 上限)
    ('生後60日(45-75日)', 45, 75),
    ('生後90日(76-105日)', 76, 105),
    ('生後120日(106-135日)', 106, 135),
    ('生後180日(165-195日)', 165, 195),
    ('生後365日(330-400日)', 330, 400),
]
MIN_N_RATE = 5

PREFS = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県',
         '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県',
         '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県',
         '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

# (チェーン名, 店舗名に対する正規表現)。上から順に最初にマッチしたもの。
CHAINS = [
    ('Coo&RIKU（クーリク）', r'coo\s*[&＆]\s*riku|クーアンドリク|クー&リク|クーリク'),
    ('ペットの専門店コジマ', r'コジマ|kojima'),
    ('ペッツファースト', r'ペッツファースト|pet\'?s\s*first|petsfirst'),
    ('AHB（ペットショップAHB）', r'\bahb\b|ＡＨＢ'),
    ('かねだい', r'かねだい|kanedai'),
    ('ペットプラス', r'ペットプラス|pet\s*plus|petplus'),
    ('ワンラブ', r'ワンラブ|wan\s*love|wanlove'),
    ('ペットワールドアミーゴ', r'アミーゴ|amigo'),
    ('DOG&CAT JOKER（ジョーカー）', r'joker|ジョーカー'),
    ('犬の家＆猫の里', r'犬の家'),
    ('ペテモ（イオンペット）', r'ペテモ|petemo|イオンペット'),
    ('ペットランド', r'ペットランド|petland'),
    ('ペッツワン', r'ペッツワン|pets\s*one|pet\'?s\s*one'),
    ('プチマリア', r'プチマリア'),
    ('ペットシティ', r'ペットシティ|pet\s*city'),
    ('P2&ASTY', r'p2\s*[&＆]\s*asty|アスティ'),
    ('ペットショップ ワンワン', r'ペットショップワンワン|ペットショップ\s+ワンワン'),
    ('ジャンボペット', r'ジャンボペット'),
    ('ペットパラダイス', r'ペットパラダイス'),
    ('ドッグ・ジャンキー', r'ジャンキー'),
    ('ひごペットフレンドリー', r'ひごペット'),
    ('マルエスペット', r'マルエスペット'),
    ('ペットアミ', r'ペットアミ(?!ーゴ)'),
    ('ワンニャンハウス', r'ワンニャンハウス'),
    ('OneBuddy', r'onebuddy|one\s*buddy'),
    ('センチュリーペット', r'センチュリーペット'),
    ('ファミリーペット', r'ファミリーペット'),
    ('ジャパンペッツ', r'ジャパンペッツ'),
    ('竹内ペット', r'竹内ペット'),
    ('ハッピーベル', r'ハッピーベル'),
    ('ペッツコンシェル', r'ペッツコンシェル'),
    ('ペットプラザ', r'ペットプラザ'),
    ('ディスワン', r'ディスワン'),
    ('DOGMAN', r'dogman'),
    ('ペッツスマイル', r'ペッツスマイル'),
    ('スタードッグス', r'スタードッグス'),
]


def chain_of(name):
    s = (name or '').lower()
    s = s.replace('　', ' ')
    for cname, pat in CHAINS:
        if re.search(pat, s, flags=re.I):
            return cname
    return ''


def pref_of(addr):
    for p in PREFS:
        if (addr or '').startswith(p):
            return p
    return ''


def parse_birth(s):
    m = re.match(r'(\d{4})年(\d{1,2})月(\d{1,2})日', s or '')
    return pd.Timestamp(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else pd.NaT


def bin_of(d):
    if pd.isna(d):
        return ''
    for lab, lo, hi in BINS:
        if lo <= d <= hi:
            return lab
    return ''


def load():
    rows = [json.loads(l) for l in open(SRC, encoding='utf-8')]
    df = pd.DataFrame(rows)
    n_raw = len(df)
    df = df.drop_duplicates('掲載URL', keep='first').copy()
    df['生年月日'] = df['誕生日'].map(parse_birth)
    df['取得日_ts'] = pd.to_datetime(df['取得日'])
    df['生後日数'] = (df['取得日_ts'] - df['生年月日']).dt.days
    df['生後日数ビン'] = df['生後日数'].map(bin_of)
    df['都道府県'] = df['住所'].map(pref_of)
    df['チェーン名'] = df['店舗名'].map(chain_of)
    df['チェーン判定区分'] = df['チェーン名'].map(lambda c: '推測' if c else '')
    df['掲載区分'] = df['店舗ラベル'].map(
        lambda l: 'ブリーダー直販' if 'ブリーダー' in (l or '') else ('ペットショップ掲載' if '店舗' in (l or '') else '不明'))
    return df, n_raw


def write(df, name):
    p = os.path.join(CLEAN, name)
    df.to_csv(p, index=False, encoding='utf-8-sig')
    print('wrote', p, len(df))


def main():
    os.makedirs(CLEAN, exist_ok=True)
    df, n_raw = load()
    print('raw rows', n_raw, 'unique', len(df))

    # ---- 明細
    det = pd.DataFrame({
        '年度または暦年': '暦年', '年': 2026,
        'サイト': df['サイト'], '掲載区分': df['掲載区分'], '犬/猫': df['犬/猫'],
        '犬種/猫種': df['対象品種'], '掲載品種表記': df['掲載品種'],
        '性別': df['性別'].replace({'男の子': 'オス', '女の子': 'メス'}),
        '生年月日': df['生年月日'].dt.strftime('%Y-%m-%d'), '生後日数': df['生後日数'], '生後日数ビン': df['生後日数ビン'],
        '価格': df['価格'], '単位': '円', '税区分': df['税区分'],
        '毛色': df['毛色'], '店舗名': df['店舗名'], 'チェーン名': df['チェーン名'], 'チェーン判定区分': df['チェーン判定区分'],
        '都道府県': df['都道府県'], '住所(市区町村)': df['住所'],
        '掲載URL': df['掲載URL'], '区分': '実測', '出典URL': df['一覧URL'], '取得日': df['取得日'],
        '備考': df['生後日数'].map(lambda x: '生年月日が取得日より後（掲載の誤記の可能性）。ビン集計対象外' if x < 0 else
                                 ('生後56日未満（動愛法の8週齢規制に照らすと生年月日誤記の可能性）' if x < 56 else '')),
    })
    write(det, '店頭価格_明細.csv')

    v = df[df['価格'].notna() & df['生後日数'].notna()]
    rows = []
    common = {'年度または暦年': '暦年', '年': 2026, 'サイト': 'ペットミー'}
    src_of = {k: f'https://petmi.jp/{p}/' for k, p in df.groupby('対象品種')['検索kind'].first().items()}
    date = df['取得日'].iloc[0]
    def rate_row(base, med, a, b, tag):
        (ma, na), (mb, nb) = med[a], med[b]
        if ma and mb and na >= MIN_N_RATE and nb >= MIN_N_RATE:
            return dict(base, 項目=f'価格下落率_{tag}', 生後日数ビン=tag.replace('生後', '').replace('日', ''),
                        値=round((ma - mb) / ma * 100, 1), 単位='%', 件数=min(na, nb), 区分='計算',
                        備考=f'(中央値[{a}]−中央値[{b}])/中央値[{a}]。n={na},{nb}。横断データ（同一個体の追跡ではない）')
        return dict(base, 項目=f'価格下落率_{tag}', 生後日数ビン=tag.replace('生後', '').replace('日', ''), 値=None, 単位='%',
                    件数=min(na, nb), 区分='計算', 備考=f'件数不足のため計算せず（n={na},{nb}、必要各{MIN_N_RATE}件以上）')

    groups = [((a, k), g, src_of[k]) for (a, k), g in v.groupby(['犬/猫', '対象品種'])]
    groups += [((a, f'{a}・対象品種計'), g, 'https://petmi.jp/') for a, g in v.groupby('犬/猫')]
    for (animal, kind), g, src in groups:
        base = dict(common, **{'犬/猫': animal, '犬種/猫種': kind, '出典URL': src, '取得日': date})
        sub = df[df['対象品種'] == kind] if kind in src_of else df[df['犬/猫'] == animal]
        rows.append(dict(base, 項目='掲載件数(重複除去後)', 生後日数ビン='全体', 値=len(sub), 単位='件', 件数=len(sub), 区分='実測',
                         備考=('一覧の総数表示=' + str(sub['一覧総数'].iloc[0])) if kind in src_of else '品種合算'))
        rows.append(dict(base, 項目='価格中央値', 生後日数ビン='全体', 値=float(g['価格'].median()), 単位='円(税込)',
                         件数=len(g), 区分='計算', 備考=''))
        med = {}
        for lab, lo, hi in BINS:
            gb = g[g['生後日数ビン'] == lab]
            m = float(gb['価格'].median()) if len(gb) else None
            med[lab] = (m, len(gb))
            note = '' if len(gb) else '該当ビンの掲載なし'
            if lab.startswith('生後365') and len(gb):
                top = gb['チェーン名'].replace('', '判定なし').value_counts()
                note = f'件数少。最多チェーン={top.index[0]}({top.iloc[0]}件)'
            rows.append(dict(base, 項目='価格中央値', 生後日数ビン=lab, 値=m, 単位='円(税込)', 件数=len(gb), 区分='計算', 備考=note))
        rows.append(rate_row(base, med, BINS[0][0], BINS[-1][0], '生後60日→365日'))
        rows.append(rate_row(base, med, BINS[0][0], BINS[3][0], '生後60日→180日'))
    # 掲載区分の内訳
    for (site, kbn), g in df.groupby(['サイト', '掲載区分']):
        rows.append(dict(common, **{'犬/猫': '犬猫計', '犬種/猫種': '対象品種計', '項目': f'掲載件数_{kbn}', '生後日数ビン': '全体',
                                    '値': len(g), '単位': '件', '件数': len(g), '区分': '実測',
                                    '出典URL': 'https://petmi.jp/', '取得日': date, '備考': 'サイト別・掲載区分別内訳'}))
    rows.append(dict(common, **{'サイト': 'ブリーダーナビ', '犬/猫': '犬', '犬種/猫種': '対象品種計', '項目': '掲載件数_ブリーダー直販',
                                '生後日数ビン': '全体', '値': None, '単位': '件', '件数': None, '区分': '実測',
                                '出典URL': 'https://www.breeder-navi.jp/term', '取得日': date,
                                '備考': '利用規約でクローリング・スクレイピング等による収集を禁止しているため取得せず'}))
    cols = ['年度または暦年', '年', 'サイト', '犬/猫', '犬種/猫種', '項目', '生後日数ビン', '値', '単位', '件数', '区分', '出典URL', '取得日', '備考']
    write(pd.DataFrame(rows)[cols], '店頭価格_中央値表.csv')

    # ---- チェーン別
    crow = []
    vv = v.copy()
    vv['チェーン'] = vv['チェーン名'].replace('', 'チェーン判定なし（個人店・その他）')
    for (animal, ch), g in vv.groupby(['犬/猫', 'チェーン']):
        crow.append(dict(common, **{'犬/猫': animal, 'チェーン名': ch, '犬種/猫種': '対象品種計', '項目': '価格中央値',
                                    '値': float(g['価格'].median()), '単位': '円(税込)', '件数': len(g),
                                    '生後日数中央値': float(g['生後日数'].median()), '店舗数': g['店舗名'].nunique(),
                                    '区分': '計算', 'チェーン判定区分': '推測' if not ch.startswith('チェーン判定なし') else '',
                                    '出典URL': 'https://petmi.jp/', '取得日': date,
                                    '備考': '品種構成・月齢構成の違いを調整していない単純中央値'}))
    for (animal, ch, kind), g in vv.groupby(['犬/猫', 'チェーン', '対象品種']):
        if len(g) < 10:
            continue
        crow.append(dict(common, **{'犬/猫': animal, 'チェーン名': ch, '犬種/猫種': kind, '項目': '価格中央値',
                                    '値': float(g['価格'].median()), '単位': '円(税込)', '件数': len(g),
                                    '生後日数中央値': float(g['生後日数'].median()), '店舗数': g['店舗名'].nunique(),
                                    '区分': '計算', 'チェーン判定区分': '推測' if not ch.startswith('チェーン判定なし') else '',
                                    '出典URL': src_of[kind], '取得日': date, '備考': '件数10以上の組合せのみ'}))
    ccols = ['年度または暦年', '年', 'サイト', '犬/猫', 'チェーン名', 'チェーン判定区分', '犬種/猫種', '項目', '値', '単位', '件数',
             '生後日数中央値', '店舗数', '区分', '出典URL', '取得日', '備考']
    write(pd.DataFrame(crow)[ccols], '店頭価格_チェーン別.csv')


if __name__ == '__main__':
    main()
