#!/usr/bin/env python3
"""アニフェア（anifare.jp）里親募集の定点観測。

使い方:
  python3 -I work/anifare_weekly.py            # 取得して差分・パネル・週報を更新
  python3 -I work/anifare_weekly.py --no-fetch # 既存スナップショットから再計算だけ
  python3 -I work/anifare_weekly.py --history  # 過去の「里親が決まりました」記事(2019-21)も取得（初回のみ）

作法: 1リクエスト3秒以上・同時接続1。robots.txt を毎回確認。ログイン・非公開ページには触らない。
生HTML/JSON は anifare/raw/YYYY-MM-DD.tar.gz に保存。
"""
import sys, os, re, io, json, time, tarfile, hashlib, datetime as dt
from pathlib import Path
import requests
import pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
AN = ROOT / "anifare"
SNAP = AN / "snapshots"
RAW = AN / "raw"
for p in (AN, SNAP, RAW):
    p.mkdir(parents=True, exist_ok=True)
BASE = "https://anifare.jp"
UA = "Mozilla/5.0 (research; contact via site)"
WAIT = 3.2
JST = dt.timezone(dt.timedelta(hours=9))
TODAY = dt.datetime.now(JST).strftime("%Y-%m-%d")
S = requests.Session()
S.headers["User-Agent"] = UA
_last = [0.0]
_raw = {}  # name -> bytes


def log(msg):
    line = f"- {dt.datetime.now(JST).strftime('%Y-%m-%d %H:%M')} JST　{msg}"
    print(line, flush=True)
    with open(AN / "log.md", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get(url, save_as=None, **kw):
    d = WAIT - (time.time() - _last[0])
    if d > 0:
        time.sleep(d)
    for attempt in range(3):
        try:
            r = S.get(url, timeout=40, **kw)
            _last[0] = time.time()
            if r.status_code in (403, 429):
                log(f"{url} が {r.status_code}。ブロックとみなし、回避せず中止")
                raise SystemExit(2)
            if save_as:
                _raw[save_as] = r.content
            return r
        except requests.RequestException as e:
            _last[0] = time.time()
            if attempt == 2:
                log(f"{url} の取得に失敗（{type(e).__name__}）")
                return None
            time.sleep(10)


def robots_ok():
    r = get(BASE + "/robots.txt", save_as="robots.txt")
    if r is None or r.status_code != 200:
        log("robots.txt を取得できず中止")
        return False
    dis, ua_all = [], False
    for ln in r.text.splitlines():
        ln = ln.split("#")[0].strip()
        if ln.lower().startswith("user-agent:"):
            ua_all = ln.split(":", 1)[1].strip() == "*"
        elif ua_all and ln.lower().startswith("disallow:"):
            v = ln.split(":", 1)[1].strip()
            if v:
                dis.append(v)
    bad = [d for d in dis if any(p.startswith(d) for p in ("/dogcat/", "/category/dog/", "/wp-json/", "/family/"))]
    log(f"robots.txt 確認：Disallow={dis}")
    if bad:
        log(f"禁止パスに該当 {bad} → 取得せず停止（判断を仰ぐ）")
        return False
    return True


def classify_origin(text):
    """出どころの分類ルール（レポートに明記）。
    ブリーダー由来: 説明文に「ブリーダー」「繁殖」「引退」のどれかがある
    家庭由来: 「飼えなくな」「飼い主」「飼育放棄」「ご家庭」「家庭の事情」「やむを得ない事情」のどれかがある
    両方に当たる→「両方の語あり」、どちらも無い→「不明」
    """
    t = text or ""
    b = bool(re.search(r"ブリーダー|繁殖|引退", t))
    h = bool(re.search(r"飼えなくな|飼い主|飼育放棄|ご家庭|家庭の事情|やむを得ない事情|やむをえない事情", t))
    if b and h:
        return "両方の語あり"
    if b:
        return "ブリーダー由来"
    if h:
        return "家庭由来"
    return "不明"


def parse_age(s):
    if not s:
        return None
    y = re.search(r"(\d+)\s*歳", s)
    m = re.search(r"(\d+)\s*[ヶか]月", s)
    if not y and not m:
        return None
    return (int(y.group(1)) if y else 0) + (int(m.group(1)) if m else 0) / 12


def parse_birth(s):
    m = re.search(r"(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日", s or "")
    return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" if m else ""


def parse_detail(html, url):
    s = BeautifulSoup(html, "html.parser")
    rec = {"掲載URL": url, "掲載ID": url.rstrip("/").split("/")[-1]}
    # 上部の 名前/犬種/年齢/場所
    body = s.get_text("\n", strip=True)
    def after(label):
        m = re.search(rf"\n{label}\n([^\n]+)\n", body)
        return m.group(1).strip() if m else ""
    name = after("名前")
    rec["名前"] = name
    rec["性別"] = "メス" if "♀" in name else ("オス" if "♂" in name else "")
    rec["犬種"] = after("犬種")
    rec["年齢表記"] = after("年齢")
    rec["年齢_歳"] = parse_age(rec["年齢表記"])
    rec["拠点"] = after("場所")
    meta = {}
    for tr in s.select("tr.meta_row"):
        th, td = tr.find("th"), tr.find("td")
        if th and td:
            meta.setdefault(th.get_text(strip=True), td.get_text(" ", strip=True))
    rec["番号"] = meta.get("番号", "")
    rec["生年月日"] = parse_birth(meta.get("生年月日", ""))
    rec["カラー"] = meta.get("カラー", "")
    rec["避妊去勢"] = meta.get("避妊・去勢", "")
    rec["体重"] = meta.get("体重", "")
    rec["混合ワクチン"] = meta.get("混合ワクチン", "")
    rec["マイクロチップ"] = meta.get("マイクロチップ", "")
    rec["募集経緯欄"] = meta.get("募集経緯", "")
    rec["持病欄"] = " / ".join(f"{k}:{v}" for k, v in meta.items() if re.search(r"病|疾患|健康|既往|治療", k))
    rec["その他の欄"] = json.dumps({k: v for k, v in meta.items() if k not in
        ("番号", "生年月日", "カラー", "避妊・去勢", "体重", "混合ワクチン", "マイクロチップ", "募集経緯")}, ensure_ascii=False)
    c = s.select_one(".staff-comment-box-left") or s.select_one(".staff-comment-box")
    rec["説明文"] = c.get_text(" ", strip=True) if c else ""
    rec["タグ"] = " / ".join(li.get_text(strip=True) for li in s.select("li[class^=custom-list]"))
    src_text = rec["説明文"] + " " + rec["募集経緯欄"]
    rec["出どころ分類"] = classify_origin(src_text)
    rec["産歴の記載"] = "あり" if re.search(r"出産|産歴|お産|帝王切開|ママ犬|母犬|お母さん犬", rec["説明文"]) else ""
    rec["持病の記載"] = "あり" if re.search(r"疾患|持病|ヘルニア|パテラ|膝蓋骨|心雑音|心臓|てんかん|白内障|腫瘍|アレルギー|皮膚|歯|投薬|治療|手術", rec["説明文"]) else ""
    # 費用・寄付の文言（そのまま）
    fee = [ln for ln in body.split("\n") if re.search(r"寄付|費用|支援金|万円|円", ln) and len(ln) < 200]
    seen, keep = set(), []
    for ln in fee:
        if ln not in seen and not re.search(r"寄付・ご支援について|個人情報", ln):
            seen.add(ln); keep.append(ln)
    rec["費用寄付の文言"] = " ｜ ".join(keep[:6])
    rec["金額の記載"] = " / ".join(sorted(set(re.findall(r"[\d,\.]+\s*万?円", " ".join(keep)))))
    up = re.search(r"(\d{4})\.(\d{1,2})\.(\d{1,2})更新", body)
    rec["取得日"] = TODAY
    return rec


def rest_all(params, tag):
    out, page = [], 1
    while True:
        q = "&".join(f"{k}={v}" for k, v in params.items())
        r = get(f"{BASE}/wp-json/wp/v2/{tag}?per_page=100&page={page}&{q}", save_as=f"rest_{tag}_{hashlib.md5(q.encode()).hexdigest()[:6]}_{page}.json")
        if r is None or r.status_code != 200:
            break
        d = r.json()
        out += d
        tp = int(r.headers.get("X-WP-TotalPages", "1"))
        if page >= tp or not d:
            break
        page += 1
    return out


def crawl():
    posts = rest_all({"categories": 2, "_fields": "id,date,modified,link,title,featured_media"}, "posts")
    log(f"REST: 里親募集（category=dogcat）{len(posts)}件")
    rows = []
    for i, p in enumerate(posts, 1):
        url = p["link"]
        r = get(url, save_as=f"dogcat_{p['id']}.html")
        if r is None or r.status_code != 200:
            log(f"{url} HTTP {getattr(r, 'status_code', '—')}")
            continue
        rec = parse_detail(r.text, url)
        rec["WP投稿ID"] = p["id"]
        rec["WP日付"] = p["date"]
        rec["WP更新"] = p["modified"]
        rec["写真ID"] = p.get("featured_media", "")
        rows.append(rec)
        if i % 40 == 0:
            print(f"  詳細 {i}/{len(posts)}", flush=True)
    df = pd.DataFrame(rows)
    return df


def calibrate(full=False):
    """WP投稿IDと「作られた日」の対応表。投稿IDは投稿・画像で共通の通し番号なので、
    画像（media）のアップロード日＝その番号が発番された日として使える。"""
    f = AN / "id_date.csv"
    old = pd.read_csv(f) if f.exists() else pd.DataFrame(columns=["id", "date", "種別"])
    rows = []
    pages = 60 if full else 3
    for page in range(1, pages + 1):
        r = get(f"{BASE}/wp-json/wp/v2/media?per_page=100&page={page}&orderby=id&order=desc&_fields=id,date", save_as=f"rest_media_{page}.json")
        if r is None or r.status_code != 200:
            break
        d = r.json()
        rows += [{"id": x["id"], "date": x["date"], "種別": "media"} for x in d]
        if not d or (len(old) and min(x["id"] for x in d) < old["id"].max() and not full):
            break
    new = pd.concat([old, pd.DataFrame(rows)]).drop_duplicates("id").sort_values("id")
    new.to_csv(f, index=False, encoding="utf-8-sig")
    log(f"ID→日付の対応表 {len(new)}点（画像のアップロード日）")
    return new


def est_created(ids, cal):
    """投稿IDより小さい直近の画像IDと、大きい直近の画像IDの日付の間。保守的に『直前の画像の日付』を使う。"""
    import bisect
    c = cal.sort_values("id")
    xs, ds = c["id"].tolist(), c["date"].tolist()
    out = []
    for i in ids:
        k = bisect.bisect_left(xs, i)
        lo = ds[k - 1] if k > 0 else None
        hi = ds[k] if k < len(xs) else None
        out.append((lo[:10] if lo else "", hi[:10] if hi else ""))
    return out


def save_raw():
    if not _raw:
        return
    path = RAW / f"{TODAY}.tar.gz"
    with tarfile.open(path, "w:gz") as tf:
        for name, b in _raw.items():
            ti = tarfile.TarInfo(name); ti.size = len(b); ti.mtime = int(time.time())
            tf.addfile(ti, io.BytesIO(b))
    log(f"生データ保存 raw/{TODAY}.tar.gz（{len(_raw)}ファイル）")


def build_panel():
    snaps = sorted(SNAP.glob("*.csv"))
    if not snaps:
        return None
    dates = [p.stem for p in snaps]
    frames = {p.stem: pd.read_csv(p, dtype=str).fillna("") for p in snaps}
    cal = pd.read_csv(AN / "id_date.csv") if (AN / "id_date.csv").exists() else None
    rows = {}
    for d in dates:
        for _, r in frames[d].iterrows():
            k = r["掲載ID"]
            if k not in rows:
                rows[k] = dict(r); rows[k]["初出日"] = d; rows[k]["観測回数"] = 0
            rows[k]["最終掲載日"] = d
            rows[k]["観測回数"] += 1
            for c in ("拠点", "説明文", "年齢表記", "体重", "出どころ分類"):
                rows[k][c] = r.get(c, rows[k].get(c, ""))
    last = dates[-1]
    out = []
    for k, r in rows.items():
        gone = r["最終掲載日"] != last
        r["状態"] = "消えた" if gone else "掲載中"
        r["初出は観測開始時点"] = r["初出日"] == dates[0]
        if gone:
            nxt = dates[dates.index(r["最終掲載日"]) + 1]
            r["消滅確認日"] = nxt
        else:
            r["消滅確認日"] = ""
        out.append(r)
    p = pd.DataFrame(out)
    if cal is not None and len(cal):
        est = est_created(p["掲載ID"].astype(int).tolist(), cal)
        p["掲載開始_推定_下限"] = [a for a, b in est]
        p["掲載開始_推定_上限"] = [b for a, b in est]
    else:
        p["掲載開始_推定_下限"] = ""; p["掲載開始_推定_上限"] = ""
    def days(a, b):
        try:
            return (pd.Timestamp(b) - pd.Timestamp(a)).days
        except Exception:
            return None
    # 滞留日数：開始＝ID からの推定日（無ければ初出日）、終了＝消えたと確認した日と最終掲載日の中間
    st = p["掲載開始_推定_下限"].where(p["掲載開始_推定_下限"] != "", p["初出日"])
    p["滞留日数_下限"] = [days(s, l) if g == "消えた" else None for s, l, g in zip(st, p["最終掲載日"], p["状態"])]
    p["滞留日数_上限"] = [days(s, c) if g == "消えた" else None for s, c, g in zip(st, p["消滅確認日"], p["状態"])]
    p["掲載中の経過日数"] = [days(s, last) if g == "掲載中" else None for s, g in zip(st, p["状態"])]
    p.to_csv(AN / "panel.csv", index=False, encoding="utf-8-sig")
    return p, dates


def weekly_report(p, dates):
    last = dates[-1]
    cur = p[p["状態"] == "掲載中"]
    lines = [f"\n## {last}"]
    lines.append(f"- 掲載中 {len(cur)}頭（取得日 {last}、出典 https://anifare.jp/category/dog/ ）")
    if len(dates) >= 2:
        prev = dates[-2]
        gap = (pd.Timestamp(last) - pd.Timestamp(prev)).days
        new = p[p["初出日"] == last]
        gone = p[p["消滅確認日"] == last]
        lines.append(f"- 前回（{prev}）から{gap}日：新規掲載 {len(new)}頭、消えた掲載 {len(gone)}頭")
        if len(gone):
            g = gone["滞留日数_上限"].dropna()
            lines.append(f"- 消えた子の滞留日数（上限、掲載開始は投稿IDからの推定）：中央値 {g.median():.0f}日、30日以内 {(g <= 30).mean() * 100:.0f}%（{(g <= 30).sum()}/{len(g)}頭）。公式は「97%が1ヶ月以内」")
        if gap:
            lines.append(f"- 新規掲載のペース：{len(new) / gap * 30:.0f}頭/月（{gap}日間の実測を30日に換算）。公式は月約500組")
    else:
        lines.append("- 初回のため差分なし")
    e = cur["掲載中の経過日数"].dropna()
    if len(e):
        lines.append(f"- 掲載中の子の経過日数（推定）：中央値 {e.median():.0f}日、30日超 {(e > 30).mean() * 100:.0f}%（{(e > 30).sum()}/{len(e)}頭）")
    with open(AN / "report_weekly.md", "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def history():
    """2019〜2021年の『里親が決まりました』記事（category=family）。本文に募集経緯欄がある。"""
    cats = get(f"{BASE}/wp-json/wp/v2/categories?per_page=100&_fields=id,slug,count", save_as="rest_categories.json").json()
    fam = [c for c in cats if c["slug"] == "family"]
    if not fam:
        log("family カテゴリが見つからない"); return
    posts = rest_all({"categories": fam[0]["id"], "_fields": "id,date,modified,link,title,content"}, "posts")
    rows = []
    for p in posts:
        s = BeautifulSoup(p["content"]["rendered"], "html.parser")
        meta = {}
        for tr in s.select("tr"):
            th, td = tr.find("th"), tr.find("td")
            if th and td:
                meta.setdefault(th.get_text(strip=True), td.get_text(" ", strip=True))
        rows.append({"WP投稿ID": p["id"], "記事日付": p["date"][:10], "URL": p["link"], "題": BeautifulSoup(p["title"]["rendered"], "html.parser").get_text(),
                     "番号": meta.get("番号", ""), "生年月日": parse_birth(meta.get("生年月日", "")), "避妊去勢": meta.get("避妊・去勢", ""),
                     "体重": meta.get("体重", ""), "募集経緯": meta.get("募集経緯", ""), "出どころ分類": classify_origin(meta.get("募集経緯", "")),
                     "取得日": TODAY})
    pd.DataFrame(rows).to_csv(AN / "history_family_2019-2021.csv", index=False, encoding="utf-8-sig")
    log(f"過去の『里親が決まりました』記事 {len(rows)}件を保存")


def main():
    a = sys.argv[1:]
    if "--no-fetch" not in a:
        if not robots_ok():
            sys.exit(1)
        df = crawl()
        if len(df) == 0:
            log("取得0件。サイト構造が変わった可能性。保存せず終了"); save_raw(); sys.exit(1)
        calibrate(full=not (AN / "id_date.csv").exists())
        if "--history" in a:
            history()
        df.to_csv(SNAP / f"{TODAY}.csv", index=False, encoding="utf-8-sig")
        log(f"スナップショット保存 snapshots/{TODAY}.csv（{len(df)}頭）")
        save_raw()
    res = build_panel()
    if res:
        weekly_report(*res)


if __name__ == "__main__":
    main()
