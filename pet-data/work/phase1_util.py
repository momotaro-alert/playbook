"""Phase1 共通ユーティリティ（スクリプトは python3 -I で実行するため、各スクリプトで sys.path に work/ を追加して import する）"""
import re, subprocess, os, csv

ROOT = '/home/user/playbook/pet-data'
RAW = os.path.join(ROOT, 'raw', 'env')
CLEAN = os.path.join(ROOT, 'clean')
TODAY = '2026-11-02'
BASE = 'https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/'

Z2H = str.maketrans('０１２３４５６７８９，', '0123456789,')

NUM_RE = re.compile(r'^(?:\d{1,3}(?:,\d{3})+|\d+)$')
MISSING = {'-', '－', '−', '‐', '―', '…', '—'}


def pdftext(path):
    return subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout


def is_num(t):
    t = t.translate(Z2H)
    return bool(NUM_RE.match(t)) or t in MISSING


def to_val(t):
    t = t.translate(Z2H)
    if t in MISSING:
        return None
    return int(t.replace(',', ''))


ERA = {'昭和': 1925, '平成': 1988, '令和': 2018}


def era_year(s):
    """'平成２５年度' -> 2013, '令和元年度' -> 2019"""
    s = s.translate(Z2H).replace(' ', '').replace('　', '')
    m = re.search(r'(昭和|平成|令和)(元|\d+)', s)
    if not m:
        return None
    n = 1 if m.group(2) == '元' else int(m.group(2))
    return ERA[m.group(1)] + n


def meta_url(path):
    """raw ファイルの .meta.txt から URL を取得"""
    with open(path + '.meta.txt') as f:
        for line in f:
            if line.startswith('URL:'):
                return line.split(':', 1)[1].strip()
    raise ValueError(path)


def split_line(line):
    """行を (名称, 数値トークンlist) に分ける。名称は先頭の非数値トークンを連結。"""
    toks = line.split()
    name = []
    i = 0
    while i < len(toks) and not is_num(toks[i]):
        name.append(toks[i])
        i += 1
    nums = toks[i:]
    return ''.join(name), nums


def write_csv(path, rows, cols):
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore')
        w.writeheader()
        for r in rows:
            w.writerow(r)


# 政令指定都市・中核市（過去に中核市だった市を含む）→ 都道府県
CITY_PREF = {
    # 指定都市
    '札幌市': '北海道', '仙台市': '宮城県', 'さいたま市': '埼玉県', '千葉市': '千葉県', '横浜市': '神奈川県',
    '川崎市': '神奈川県', '相模原市': '神奈川県', '新潟市': '新潟県', '静岡市': '静岡県', '浜松市': '静岡県',
    '名古屋市': '愛知県', '京都市': '京都府', '大阪市': '大阪府', '堺市': '大阪府', '神戸市': '兵庫県',
    '岡山市': '岡山県', '広島市': '広島県', '北九州市': '福岡県', '福岡市': '福岡県', '熊本市': '熊本県',
    # 中核市（現・旧）
    '旭川市': '北海道', '函館市': '北海道', '青森市': '青森県', '八戸市': '青森県', '盛岡市': '岩手県',
    '秋田市': '秋田県', '山形市': '山形県', '郡山市': '福島県', 'いわき市': '福島県', '福島市': '福島県',
    '水戸市': '茨城県', '宇都宮市': '栃木県', '前橋市': '群馬県', '高崎市': '群馬県', '川越市': '埼玉県',
    '越谷市': '埼玉県', '川口市': '埼玉県', '船橋市': '千葉県', '柏市': '千葉県', '八王子市': '東京都',
    '横須賀市': '神奈川県', '富山市': '富山県', '金沢市': '石川県', '福井市': '福井県', '甲府市': '山梨県',
    '長野市': '長野県', '松本市': '長野県', '岐阜市': '岐阜県', '豊橋市': '愛知県', '岡崎市': '愛知県',
    '豊田市': '愛知県', '一宮市': '愛知県', '大津市': '滋賀県', '豊中市': '大阪府', '高槻市': '大阪府',
    '枚方市': '大阪府', '東大阪市': '大阪府', '八尾市': '大阪府', '寝屋川市': '大阪府', '吹田市': '大阪府',
    '姫路市': '兵庫県', '尼崎市': '兵庫県', '明石市': '兵庫県', '西宮市': '兵庫県', '奈良市': '奈良県',
    '和歌山市': '和歌山県', '鳥取市': '鳥取県', '松江市': '島根県', '倉敷市': '岡山県', '呉市': '広島県',
    '福山市': '広島県', '下関市': '山口県', '高松市': '香川県', '松山市': '愛媛県', '高知市': '高知県',
    '久留米市': '福岡県', '長崎市': '長崎県', '佐世保市': '長崎県', '大分市': '大分県', '宮崎市': '宮崎県',
    '鹿児島市': '鹿児島県', '那覇市': '沖縄県', '徳島市': '徳島県', '佐賀市': '佐賀県', '津市': '三重県',
    '四日市市': '三重県', '山口市': '山口県', '春日井市': '愛知県', '所沢市': '埼玉県',
}

PREFS = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県',
         '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県',
         '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県',
         '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県',
         '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']


def norm_name(n):
    n = re.sub(r'[\s　]', '', n)
    n = re.sub(r'[※＊\*（(][^）)]*[）)]?$', '', n)
    n = n.rstrip('※＊*')
    n = re.sub(r'[※＊\*]\d*$', '', n)
    return n


def pref_of(name):
    if name in PREFS:
        return name
    return CITY_PREF.get(name)


def kind_of(name):
    if name in PREFS:
        return '都道府県'
    if name in ('札幌市', '仙台市', 'さいたま市', '千葉市', '横浜市', '川崎市', '相模原市', '新潟市', '静岡市',
                '浜松市', '名古屋市', '京都市', '大阪市', '堺市', '神戸市', '岡山市', '広島市', '北九州市',
                '福岡市', '熊本市'):
        return '指定都市'
    if name in CITY_PREF:
        return '中核市'
    return '不明'


def resolve_name(n):
    """縦書き見出し「都道府県等名」の文字が名称列に混入するケース（例: '府滋賀県'）を除去"""
    n = norm_name(n)
    if pref_of(n) or n == '合計':
        return n
    m = n
    while m and m[0] in '都道府県等名政令指定市中核' and not pref_of(m):
        m = m[1:]
    if not pref_of(m) and pref_of(m + '県'):
        m = m + '県'   # 例: '鹿児島'（原表の表記ゆれ）
    return m if pref_of(m) else n
