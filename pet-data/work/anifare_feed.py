#!/usr/bin/env python3
"""アニフェア定点観測（サイトが機械向けに公開している配信物だけを読む版）。

読むもの:
  1. robots.txt
  2. サイトマップ（robots.txt の Sitemap: 行でロボット向けに案内されているもの）… 掲載中の全ページのIDと更新日時
  3. RSSフィード /category/dogcat/feed/ （--rss を付けたときだけ）… 1頭ごとの番号・生年月日・避妊去勢・体重・説明文
読まないもの: 個別の犬のページ（/dogcat/ID/）、一覧ページ、検索、REST API。
  → 利用規約の禁止事項「スクレイピングなど本サイト上の情報を不適切な方法で取得する行為」に配慮し、
     HTMLページの解析（スクレイピング）はしない。

  python3 -I work/anifare_feed.py            # サイトマップだけ（週2〜3リクエスト）
  python3 -I work/anifare_feed.py --rss      # ＋RSS（週 約20リクエスト）
  python3 -I work/anifare_feed.py --no-fetch # 再集計だけ
1リクエスト3秒以上・同時接続1。取得した生のXMLは anifare/raw/feed_YYYY-MM-DD.tar.gz に保存。
"""
import sys, re, io, time, tarfile, html, datetime as dt
from email.utils import parsedate_to_datetime
from pathlib import Path
import requests, pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
AN = ROOT / "anifare"; SNAP = AN / "snapshots"; RAW = AN / "raw"
for p in (AN, SNAP, RAW):
    p.mkdir(parents=True, exist_ok=True)
BASE = "https://anifare.jp"
UA = "Mozilla/5.0 (research; contact via site)"
WAIT = 3.2
JST = dt.timezone(dt.timedelta(hours=9))
TODAY = dt.datetime.now(JST).strftime("%Y-%m-%d")
S = requests.Session(); S.headers["User-Agent"] = UA
raw, _last = {}, [0.0]


def log(m):
    line = f"- {dt.datetime.now(JST).strftime('%Y-%m-%d %H:%M')} JST　{m}"
    print(line, flush=True)
    with open(AN / "log.md", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get(u, name):
    d = WAIT - (time.time() - _last[0])
    if d > 0:
        time.sleep(d)
    r = S.get(u, timeout=40); _last[0] = time.time()
    if r.status_code in (403, 429):
        log(f"{u} が {r.status_code}。ブロックとみなし、回避せず中止"); raise SystemExit(2)
    raw[name] = r.content
    return r


def classify_origin(t):
    """出どころの分類ルール:
    ブリーダー由来 = 説明文に「ブリーダー」「繁殖」「引退」のどれか
    家庭由来 = 「飼えなくな」「飼い主」「飼育放棄」「ご家庭」「家庭の事情」「やむを得ない事情」のどれか
    両方→「両方の語あり」、どちらも無い→「不明」"""
    t = t or ""
    b = bool(re.search(r"ブリーダー|繁殖|引退", t))
    h = bool(re.search(r"飼えなくな|飼い主|飼育放棄|ご家庭|家庭の事情|やむを得ない事情|やむをえない事情", t))
    return "両方の語あり" if b and h else "ブリーダー由来" if b else "家庭由来" if h else "不明"


def sitemap():
    r = get(BASE + "/robots.txt", "robots.txt")
    sm = re.findall(r"(?im)^sitemap:\s*(\S+)", r.text)
    dis = re.findall(r"(?im)^disallow:\s*(\S+)", r.text)
    log(f"robots.txt 確認：Sitemap={sm}、Disallow={dis}")
    if not sm:
        log("robots.txt に Sitemap の案内がない → 中止"); raise SystemExit(1)
    idx = get(sm[0], "sitemaps.xml").text
    rows = []
    for loc in re.findall(r"<loc>([^<]+post-sitemap\d*\.xml)</loc>", idx):
        x = get(loc, loc.rsplit("/", 1)[-1]).text
        for u, lm in re.findall(r"<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]+)</lastmod>)?", x):
            m = re.match(rf"{BASE}/dogcat/(\d+)/", u)
            if m:
                rows.append({"掲載ID": m.group(1), "掲載URL": u, "サイトマップ更新日時": lm, "取得日": TODAY})
        if rows and "post-sitemap1" in loc:
            break  # 2・3 は 2020〜21年の古い記事だけ（更新日時で確認済み）
    df = pd.DataFrame(rows).drop_duplicates("掲載ID")
    log(f"サイトマップ：里親募集ページ {len(df)}件")
    return df


def rss(n_expected):
    rows, page = [], 1
    while page <= 40:
        r = get(f"{BASE}/category/dogcat/feed/?paged={page}", f"feed_{page}.xml")
        if r.status_code != 200:
            break
        items = re.findall(r"<item>(.*?)</item>", r.text, re.S)
        if not items:
            break
        for it in items:
            link = re.search(r"<link>([^<]+)</link>", it).group(1)
            pub = re.search(r"<pubDate>([^<]+)</pubDate>", it)
            body = re.search(r"<content:encoded><!\[CDATA\[(.*?)\]\]></content:encoded>", it, re.S)
            s = BeautifulSoup(body.group(1) if body else "", "html.parser")
            meta = {tr.find("th").get_text(strip=True): tr.find("td").get_text(" ", strip=True)
                    for tr in s.select("tr") if tr.find("th") and tr.find("td")}
            c = s.select_one(".staff-comment-box-left")
            text = c.get_text(" ", strip=True) if c else ""
            b = re.search(r"(\d{4})年\s*(\d{1,2})月\s*(\d{1,2})日", meta.get("生年月日", ""))
            m = re.match(r"^(.+?)の(.+?)(ちゃん|くん|君)です", text)
            rows.append({
                "掲載ID": link.rstrip("/").split("/")[-1], "掲載URL": link, "番号": meta.get("番号", ""),
                "RSS配信日時": parsedate_to_datetime(pub.group(1)).astimezone(JST).strftime("%Y-%m-%d %H:%M") if pub else "",
                "犬種_説明文から": m.group(1).strip() if m else "", "名前_説明文から": m.group(2).strip() if m else "",
                "生年月日": f"{b.group(1)}-{int(b.group(2)):02d}-{int(b.group(3)):02d}" if b else "",
                "カラー": meta.get("カラー", ""), "避妊去勢": meta.get("避妊・去勢", ""), "体重": meta.get("体重", ""),
                "説明文": text, "出どころ分類": classify_origin(text),
                "産歴の記載": "あり" if re.search(r"出産|産歴|お産|帝王切開|ママ犬|母犬", text) else "",
                "持病の記載": "あり" if re.search(r"疾患|持病|ヘルニア|パテラ|膝蓋骨|心雑音|心臓|てんかん|白内障|腫瘍|アレルギー|投薬|治療中|手術", text) else "",
                "金額の記載": " / ".join(sorted(set(re.findall(r"[\d,\.]+\s*万?円", text)))),
                "その他の欄": "; ".join(f"{k}:{v}" for k, v in meta.items() if k not in ("番号", "生年月日", "カラー", "避妊・去勢", "体重")),
            })
        if len(items) < 10 or len(rows) >= n_expected + 20:
            break
        page += 1
    df = pd.DataFrame(rows).drop_duplicates("掲載ID")
    log(f"RSS：{len(df)}頭（{page}ページ）")
    return df


def save_raw():
    with tarfile.open(RAW / f"feed_{TODAY}.tar.gz", "w:gz") as tf:
        for n, b in raw.items():
            ti = tarfile.TarInfo(n); ti.size = len(b); ti.mtime = int(time.time()); tf.addfile(ti, io.BytesIO(b))


def build_panel():
    snaps = sorted(SNAP.glob("*.csv"))
    if not snaps:
        return None
    dates = [p.stem for p in snaps]
    rows = {}
    for p in snaps:
        d = p.stem
        for r in pd.read_csv(p, dtype=str).fillna("").to_dict("records"):
            k = r["掲載ID"]
            if k not in rows:
                rows[k] = {"掲載ID": k, "初出日": d, "観測回数": 0}
            for c, v in r.items():
                if v != "" and c not in ("取得日",):
                    rows[k][c] = v
            rows[k]["最終掲載日"] = d; rows[k]["観測回数"] += 1
    last = dates[-1]
    out = []
    for r in rows.values():
        gone = r["最終掲載日"] != last
        r["状態"] = "消えた" if gone else "掲載中"
        r["消滅確認日"] = dates[dates.index(r["最終掲載日"]) + 1] if gone else ""
        r["初出は観測開始時点"] = r["初出日"] == dates[0]
        d0 = pd.Timestamp(r["初出日"])
        # 滞留日数：観測開始後に初めて現れた子だけ、下限＝最終掲載日−初出日、上限＝消滅確認日−前回観測日（初出の前の回）
        if gone and not r["初出は観測開始時点"]:
            prev_of_first = dates[dates.index(r["初出日"]) - 1]
            r["滞留日数_下限"] = (pd.Timestamp(r["最終掲載日"]) - d0).days
            r["滞留日数_上限"] = (pd.Timestamp(r["消滅確認日"]) - pd.Timestamp(prev_of_first)).days
        r["掲載中の観測日数"] = (pd.Timestamp(last) - d0).days if not gone else ""
        out.append(r)
    p = pd.DataFrame(out)
    p.to_csv(AN / "panel.csv", index=False, encoding="utf-8-sig")
    return p, dates


def report(p, dates):
    last = dates[-1]
    cur = p[p["状態"] == "掲載中"]
    L = [f"\n## {last}", f"- 掲載中 {len(cur)}頭（サイトマップ、取得日 {last}）"]
    if len(dates) >= 2:
        prev = dates[-2]; gap = (pd.Timestamp(last) - pd.Timestamp(prev)).days
        new = p[p["初出日"] == last]; gone = p[p["消滅確認日"] == last]
        L.append(f"- 前回（{prev}）から{gap}日：新規掲載 {len(new)}頭、消えた掲載 {len(gone)}頭")
        if gap:
            L.append(f"- 新規掲載のペース：{len(new) / gap * 30:.0f}頭/月（{gap}日間の実測を30日に換算）。公式は「月間506組」（2026年10月実績、https://anifare.jp/offer/ ）")
            L.append(f"- 消えたペース：{len(gone) / gap * 30:.0f}頭/月（同上）")
        allgone = p[(p["状態"] == "消えた") & (~p["初出は観測開始時点"].astype(bool))]
        if len(allgone):
            up = pd.to_numeric(allgone["滞留日数_上限"])
            L.append(f"- 観測開始後に載って消えた子 {len(allgone)}頭：滞留日数の上限が30日以内 {(up <= 30).mean() * 100:.0f}%（{(up <= 30).sum()}/{len(allgone)}）。公式は「97%が1ヶ月以内」")
        stay = pd.to_numeric(cur["掲載中の観測日数"])
        L.append(f"- 掲載中のうち、観測開始（{dates[0]}）からずっと載っている子：{(cur['初出日'] == dates[0]).sum()}頭")
    else:
        L.append("- 初回のため差分なし")
    with open(AN / "report_weekly.md", "a", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    a = sys.argv[1:]
    if "--no-fetch" not in a:
        df = sitemap()
        if len(df) == 0:
            log("サイトマップに里親募集ページが0件。構造が変わった可能性。保存せず終了"); save_raw(); sys.exit(1)
        if "--rss" in a:
            f = rss(len(df))
            df = df.merge(f.drop(columns=["掲載URL"]), on="掲載ID", how="left")
            log(f"サイトマップ {len(df)}件のうち RSS で中身が取れたのは {df['番号'].notna().sum()}件")
        df.to_csv(SNAP / f"{TODAY}.csv", index=False, encoding="utf-8-sig")
        save_raw()
        log(f"スナップショット保存 snapshots/{TODAY}.csv（{len(df)}頭）")
    res = build_panel()
    if res:
        report(*res)


if __name__ == "__main__":
    main()
