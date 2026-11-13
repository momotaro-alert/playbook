#!/usr/bin/env python3
"""ペットミー定点観測（週1回）。店頭から子犬・子猫がいつ消えるかを、同じ個体を追って実測する。

使い方（リポジトリの pet-data/ で）:
  python3 -I work/petmi_weekly.py            # 取得 → 消えた個体の確認 → panel 更新 → 週報 → 図
  python3 -I work/petmi_weekly.py --no-fetch # 取得せず、既存のスナップショットから再計算だけ
  python3 -I work/petmi_weekly.py --init0    # 第0回（2026-11-02 の clean/店頭価格_明細.csv）を snapshots に取り込む

ルール（指示書 §2）:
- 一覧 https://petmi.jp/dog/ と /cat/ を最後のページまで（全品種・全店舗）。1リクエスト2.5秒、同時接続1。
- 毎回 robots.txt を確認。/dog/ /cat/ /…/detail/ が Disallow になっていたら止めて log に書く。
- 生HTMLは保存しない。抽出結果の CSV だけ保存。
- 一覧から消えた個体は、詳細ページを1回だけ開いて状態を確認する（一覧のページ送り中のズレで
  『見落としただけ』の個体を消滅と数えないため）。
出力:
  petmi/snapshots/YYYY-MM-DD.csv, petmi/panel.csv, petmi/report_weekly.md, petmi/log.md
  charts/15_掲載消滅の日齢分布.png, charts/16_消滅直前の価格.png（スナップショット4回以上で出力）
"""
import argparse, datetime, glob, hashlib, os, re, sys, time
import pandas as pd
import requests
from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from phase4_analyze import chain_of, pref_of  # noqa: E402

ROOT = os.path.dirname(HERE)
PM = os.path.join(ROOT, "petmi")
SNAP = os.path.join(PM, "snapshots")
UA = "Mozilla/5.0 (research; contact via site)"
WAIT = 2.5
JST = datetime.timezone(datetime.timedelta(hours=9))
TODAY = datetime.datetime.now(JST).date().isoformat()
BASE0 = "2026-11-02"  # 第0回（前回調査）。20品種のみ

sess = requests.Session()
sess.headers["User-Agent"] = UA
_last = [0.0]


def log(msg):
    os.makedirs(PM, exist_ok=True)
    with open(os.path.join(PM, "log.md"), "a", encoding="utf-8") as f:
        f.write(f"- {datetime.datetime.now(JST):%Y-%m-%d %H:%M} JST　{msg}\n")
    print(msg, flush=True)


def get(url):
    dt = time.time() - _last[0]
    if dt < WAIT:
        time.sleep(WAIT - dt)
    for attempt in range(3):
        try:
            r = sess.get(url, timeout=40)
            _last[0] = time.time()
            if r.status_code in (429, 503):
                time.sleep(30 * (attempt + 1))
                continue
            return r
        except requests.RequestException as e:
            _last[0] = time.time()
            print("ERR", url, e, file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    return None


def robots_ok():
    r = get("https://petmi.jp/robots.txt")
    if r is None or r.status_code != 200:
        log(f"robots.txt を取得できなかった（{getattr(r, 'status_code', 'ERR')}）。安全のため停止")
        return False
    dis = []
    agent_all = False
    for line in r.text.splitlines():
        line = line.split("#")[0].strip()
        if line.lower().startswith("user-agent:"):
            agent_all = line.split(":", 1)[1].strip() == "*"
        elif agent_all and line.lower().startswith("disallow:"):
            dis.append(line.split(":", 1)[1].strip())
    for path in ["/dog/", "/cat/", "/dog/detail/", "/cat/detail/"]:
        for d in dis:
            if d and (d == "/" or path.startswith(d)):
                log(f"robots.txt が {path} を Disallow（{d}）に変更。取得を停止した")
                return False
    log(f"robots.txt 確認：Disallow={dis}（一覧・詳細は対象外）")
    return True


def parse_posted(s, today):
    """'2日前' '5時間前' '3週間前' '2か月前' → 掲載日の目安（ISO日付）。"""
    if not s:
        return ""
    t = datetime.date.fromisoformat(today)
    m = re.search(r"(\d+)\s*(分|時間|日|週間|か月|ヶ月|ヵ月|年)前", s)
    if not m:
        m2 = re.search(r"(\d{4})[/年.-](\d{1,2})[/月.-](\d{1,2})", s)
        return f"{int(m2.group(1)):04d}-{int(m2.group(2)):02d}-{int(m2.group(3)):02d}" if m2 else ""
    n, u = int(m.group(1)), m.group(2)
    days = {"分": 0, "時間": 0, "日": n, "週間": 7 * n, "か月": 30 * n, "ヶ月": 30 * n, "ヵ月": 30 * n, "年": 365 * n}[u]
    return (t - datetime.timedelta(days=days)).isoformat()


def jdate(s):
    m = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", s or "")
    return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}-{int(m.group(3)):02d}" if m else ""


def parse_cards(html, animal):
    s = BeautifulSoup(html, "html.parser")
    out = []
    for c in s.select("div.card"):
        a = c.select_one('.main a[href*="/detail/"]')
        if not a:
            continue
        url = "https://petmi.jp" + a["href"]
        pid = a["href"].rstrip("/").split("/")[-1]
        rec = {"個体ID": pid, "動物": animal, "掲載URL": url,
               "品種": c.select_one(".kind").get_text(strip=True) if c.select_one(".kind") else ""}
        vals = {}
        price, price_txt = None, ""
        for row in c.select(".info .row"):
            if "price-row" in (row.get("class") or []):
                price_txt = row.get_text("", strip=True)
                p = row.select_one(".price")
                if p and re.search(r"\d", p.get_text()):
                    price = int(re.sub(r"[^\d]", "", p.get_text()))
            else:
                lab = row.select_one(".label"); v = row.select_one(".value")
                vals[lab.get_text(strip=True) if lab else ""] = v.get_text(strip=True) if v else ""
        rec["性別"] = {"女の子": "メス", "男の子": "オス"}.get(vals.get("性別", ""), vals.get("性別", ""))
        rec["生年月日"] = jdate(vals.get("誕生日", ""))
        rec["毛色"] = vals.get("毛色", "")
        rec["住所"] = vals.get("住所", "")
        rec["都道府県"] = pref_of(vals.get("住所", ""))
        rec["価格"] = price
        rec["価格表示"] = price_txt
        sn = c.select_one(".shop-name")
        if sn:
            lab = sn.select_one(".shop-label")
            if lab:
                lab.extract()
            rec["店舗名"] = sn.get_text(strip=True)
        else:
            rec["店舗名"] = ""
        rec["チェーン名"] = chain_of(rec["店舗名"])
        card_txt = c.get_text(" ", strip=True)
        st = re.findall(r"(ご家族が決まりました|家族が決まりました|商談中|SOLD|売約済)", card_txt)
        rec["ステータス"] = st[0] if st else ""
        rec["バッジ"] = "|".join(b.get_text(strip=True) for b in c.select(".badge"))
        posted = c.select_one(".posted").get_text(strip=True) if c.select_one(".posted") else ""
        rec["掲載経過"] = posted
        rec["掲載日_目安"] = parse_posted(posted, TODAY)
        img = c.select_one("img.js-pet-image")
        src = img["src"] if img and img.has_attr("src") else ""
        fname = src.rstrip("/").split("/")[-1] if src else ""
        rec["写真ハッシュ"] = hashlib.sha1(fname.encode()).hexdigest()[:12] if fname else ""
        rec["取得日"] = TODAY
        out.append(rec)
    return out


def crawl():
    rows = []
    for animal, path in [("犬", "dog"), ("猫", "cat")]:
        base = f"https://petmi.jp/{path}/"
        r = get(base)
        if r is None or r.status_code != 200:
            log(f"{base} の取得に失敗（{getattr(r, 'status_code', 'ERR')}）")
            continue
        m = re.search(r"全<b>([\d,]+)</b>頭", r.text)
        total = int(m.group(1).replace(",", "")) if m else None
        pages = -(-total // 30) if total else 2000
        got = 0
        for pg in range(1, pages + 3):
            if pg > 1:
                r = get(f"{base}?page={pg}")
            if r is None or r.status_code != 200:
                if pg <= pages:
                    log(f"{base}?page={pg} の取得に失敗（{getattr(r, 'status_code', 'ERR')}）")
                break
            recs = parse_cards(r.text, animal)
            if not recs:
                break
            for x in recs:
                x["一覧ページ"] = pg
            rows += recs
            got += len(recs)
            if pg % 50 == 0:
                print(f"  {animal} {pg}/{pages}ページ {got}件", flush=True)
        log(f"{animal}：サイト表示の総数 {total}、取得カード {got}件（{pg}ページまで）")
    df = pd.DataFrame(rows)
    n0 = len(df)
    df = df.drop_duplicates("個体ID", keep="first")
    log(f"重複除去 {n0}→{len(df)}件（ページ送り中の並び替わりで同じ子が2回出た分）")
    return df


def check_detail(url):
    """一覧から消えた個体の詳細ページを1回開き、状態を返す。"""
    r = get(url)
    if r is None:
        return "取得失敗", None, ""
    if r.status_code in (404, 410):
        return "ページ削除", None, str(r.status_code)
    if r.status_code != 200:
        return "取得失敗", None, str(r.status_code)
    t = r.text
    if re.search(r"ご家族が決まりました|家族が決まりました|売約済|SOLD", t):
        return "決まりました表示", None, "200"
    if re.search(r"掲載(は)?終了|販売終了|現在.*掲載されていません|お探しのページ", t):
        return "掲載終了表示", None, "200"
    s = BeautifulSoup(t, "html.parser")
    p = s.select_one(".price")
    price = int(re.sub(r"[^\d]", "", p.get_text())) if p and re.search(r"\d", p.get_text()) else None
    if price is None:
        return "価格なし・お問い合わせ", None, "200"
    return "掲載継続（一覧で見落とし）", price, "200"


def init0():
    """第0回：2026-11-02 の明細（20品種）を snapshot 形式で保存。"""
    d = pd.read_csv(os.path.join(ROOT, "clean", "店頭価格_明細.csv"))
    o = pd.DataFrame({
        "個体ID": d["掲載URL"].str.rstrip("/").str.split("/").str[-1],
        "動物": d["犬/猫"], "掲載URL": d["掲載URL"], "品種": d["掲載品種表記"], "性別": d["性別"],
        "生年月日": d["生年月日"], "毛色": d["毛色"], "住所": d["住所(市区町村)"], "都道府県": d["都道府県"],
        "価格": d["価格"], "価格表示": "", "店舗名": d["店舗名"], "チェーン名": d["チェーン名"].fillna(""),
        "ステータス": "", "バッジ": "", "掲載経過": "", "掲載日_目安": "", "写真ハッシュ": "", "取得日": BASE0,
        "一覧ページ": "", "確認方法": "第0回（前回調査・20品種のみ）"})
    os.makedirs(SNAP, exist_ok=True)
    o.to_csv(os.path.join(SNAP, f"{BASE0}.csv"), index=False, encoding="utf-8-sig")
    log(f"第0回 {BASE0}：clean/店頭価格_明細.csv から {len(o)}件を取り込み（対象20品種のみ。他品種は第1回が初出）")


def load_snaps():
    fs = sorted(glob.glob(os.path.join(SNAP, "*.csv")))
    return {os.path.basename(f)[:10]: pd.read_csv(f, dtype={"個体ID": str}) for f in fs}


def build_panel(snaps):
    dates = sorted(snaps)
    hist = pd.concat([s.assign(回=d) for d, s in snaps.items()], ignore_index=True)
    last = dates[-1]
    rows = []
    gone_info = {}
    gp = os.path.join(PM, "disappeared.csv")
    if os.path.exists(gp):
        g = pd.read_csv(gp, dtype={"個体ID": str})
        gone_info = g.drop_duplicates("個体ID", keep="last").set_index("個体ID").to_dict("index")
    cover0 = set(snaps[BASE0]["品種"].unique()) if BASE0 in snaps else set()
    for pid, h in hist.sort_values("回").groupby("個体ID"):
        h = h.sort_values("回")
        f, l = h.iloc[0], h.iloc[-1]
        prices = h["価格"].dropna().astype(int).tolist()
        drops = sum(1 for a, b in zip(prices, prices[1:]) if b < a)
        present = l["回"] == last
        gi = gone_info.get(pid, {})
        kind = ""
        if not present:
            st = gi.get("確認結果", "")
            if (h["ステータス"].fillna("").str.contains("決まり|売約|SOLD")).any() or st == "決まりました表示":
                kind = "販売（決まりました表示）"
            elif st == "価格なし・お問い合わせ" or (h["価格"].isna().iloc[-1] if len(h) else False):
                kind = "要注目（価格なし・お問い合わせ）"
            elif st in ("ページ削除", "掲載終了表示"):
                kind = f"不明（{st}）"
            elif st:
                kind = f"不明（{st}）"
            else:
                kind = "不明（未確認）"
        bday = l.get("生年月日")
        lastseen = l["回"]
        first_seen = f["回"]
        left_cens = first_seen == dates[0] or (
            len(dates) > 1 and dates[0] == BASE0 and first_seen == dates[1] and f["品種"] not in cover0)
        def dd(a, b):
            try:
                return (datetime.date.fromisoformat(a) - datetime.date.fromisoformat(b)).days
            except Exception:
                return None
        rows.append(dict(
            個体ID=pid, 動物=l["動物"], 品種=l["品種"], 性別=l["性別"], 生年月日=bday, チェーン名=l.get("チェーン名", ""),
            店舗名=l["店舗名"], 都道府県=l["都道府県"], 初出日=first_seen,
            掲載日_目安=next((x for x in h["掲載日_目安"].fillna("") if x), ""),
            最終掲載日=lastseen, 初出価格=prices[0] if prices else None, 最終価格=prices[-1] if prices else None,
            値下げ回数=drops, 値下げ幅=(prices[0] - prices[-1]) if prices else None,
            観測回数=len(h), 掲載日数=dd(lastseen, first_seen), 消滅日齢=dd(lastseen, bday) if not present else None,
            現在日齢=dd(last, bday) if present else None, 状態="掲載中" if present else "消滅",
            消滅確認日=gi.get("確認日", "") if not present else "", 消滅種別=kind,
            初出は観測開始時点=bool(left_cens), 写真ハッシュ=l.get("写真ハッシュ", ""), 掲載URL=l["掲載URL"]))
    panel = pd.DataFrame(rows)
    panel.to_csv(os.path.join(PM, "panel.csv"), index=False, encoding="utf-8-sig")
    return panel


def weekly_report(snaps, panel, newly_gone, checked):
    dates = sorted(snaps)
    cur, prev = dates[-1], dates[-2] if len(dates) > 1 else None
    s_cur = snaps[cur]
    new_ids = set(s_cur["個体ID"]) - set().union(*[set(snaps[d]["個体ID"]) for d in dates[:-1]]) if prev else set()
    g = panel[panel["個体ID"].isin(newly_gone)]
    lines = [f"\n## {cur}（前回 {prev}）\n"]
    if prev:
        p_prev = snaps[prev].set_index("個体ID")["価格"]
        p_cur = s_cur.set_index("個体ID")["価格"]
        both = p_prev.index.intersection(p_cur.index)
        down = int(((p_cur[both] < p_prev[both]) & p_prev[both].notna()).sum())
        gap = (datetime.date.fromisoformat(cur) - datetime.date.fromisoformat(prev)).days
        for a in ["犬", "猫"]:
            ga = g[g["動物"] == a]
            sold = (ga["消滅種別"].str.startswith("販売")).mean() * 100 if len(ga) else float("nan")
            lines.append(
                f"- **{a}**：{gap}日間で {len(ga):,}件消えた。消えた個体の日齢中央値 {ga['消滅日齢'].median():.0f}日、"
                f"消滅直前価格の中央値 {ga['最終価格'].median() / 1e4:.1f}万円、『決まりました』表示だったのは {sold:.0f}%"
                if len(ga) else f"- **{a}**：消えた個体なし")
        lines.append(f"- 新規掲載 {len(new_ids):,}件、値下げ {down:,}件、掲載中 {len(s_cur):,}件（取得日 {cur}）")
        if checked:
            c = pd.Series(checked).value_counts()
            lines.append("- 一覧から消えた個体の詳細ページ確認：" + "、".join(f"{k} {v:,}件" for k, v in c.items()))
        if prev == BASE0:
            lines.append(f"- 注意：第0回（{BASE0}）は前回調査の20品種のみ。比較はその20品種の個体に限られる。"
                         f"前回からの間隔は{gap}日で、『1週間』ではない")
    p = os.path.join(PM, "report_weekly.md")
    head = "" if os.path.exists(p) else ("# ペットミー定点観測 週報\n\n出典：ペットミー掲載情報（https://petmi.jp/）。"
                                          "各回の取得日を見出しに記載。消滅種別は詳細ページを1回確認した結果。\n")
    with open(p, "a", encoding="utf-8") as f:
        f.write(head + "\n".join(lines) + "\n")
    print("\n".join(lines))


def charts(panel, n_snap, force=False):
    if n_snap < 4 and not force:
        log(f"スナップショット {n_snap}回：4回未満のため図15・16はまだ出さない")
        return
    sys.path.insert(0, HERE)
    from chartlib import DOG, CAT, DOG_L, CAT_L, finish, plt  # noqa
    import numpy as np
    g = panel[(panel["状態"] == "消滅") & panel["消滅日齢"].notna()]
    rng = f"{panel['初出日'].min()}〜{panel['最終掲載日'].max()}（{n_snap}回）"
    src = f"ペットミー掲載情報 https://petmi.jp/ の定点観測 {rng}。消滅＝一覧から消え、詳細ページでも掲載継続が確認できなかった個体"
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=False)
    for ax, a, col in [(axes[0], "犬", DOG), (axes[1], "猫", CAT)]:
        x = g[g["動物"] == a]
        bins = np.arange(0, 400, 10)
        for k, c, lab in [("販売", col, "『決まりました』表示で消えた"), ("不明", "#8a8984", "表示なしで消えた"), ("要注目", "#5f5e5a", "価格なし・お問い合わせで消えた")]:
            v = x[x["消滅種別"].str.startswith(k)]["消滅日齢"].clip(upper=395)
            ax.hist(v, bins=bins, color=c, alpha=0.85, label=f"{lab}（{len(v):,}件）", histtype="stepfilled" if k == "販売" else "step", lw=2)
        if len(x):
            ax.axvline(x["消滅日齢"].median(), color="#0b0b0b", lw=1, ls="--")
            ax.text(x["消滅日齢"].median() + 3, ax.get_ylim()[1] * 0.9, f"中央値 {x['消滅日齢'].median():.0f}日", fontsize=9)
        ax.set_title(f"{a}（消えた {len(x):,}件）", loc="left", color=col, fontsize=13)
        ax.set_xlabel("消えたときの日齢（最終掲載日−生年月日、日）"); ax.legend(frameon=False, fontsize=8.5)
    axes[0].set_ylabel("件数")
    med_d = g[g["動物"] == "犬"]["消滅日齢"].median(); med_c = g[g["動物"] == "猫"]["消滅日齢"].median()
    finish(fig, f"店頭から消えるのは、犬で生後{med_d:.0f}日・猫で生後{med_c:.0f}日前後（中央値）", src,
           os.path.join(ROOT, "charts", "15_掲載消滅の日齢分布.png"))
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
    for ax, a, col in [(axes[0], "犬", DOG), (axes[1], "猫", CAT)]:
        x = g[(g["動物"] == a) & g["初出価格"].notna() & g["最終価格"].notna()]
        ax.scatter(x["初出価格"] / 1e4, x["最終価格"] / 1e4, s=6, alpha=0.35, color=col, lw=0)
        mx = 80
        ax.plot([0, mx], [0, mx], color="#8a8984", lw=1, ls="--"); ax.text(mx * 0.62, mx * 0.66, "値下げなし", fontsize=8, color="#52514e", rotation=35)
        r = (x["最終価格"] / x["初出価格"]).median() if len(x) else float("nan")
        ax.text(2, mx * 0.9, f"最終÷初出の中央値 {r:.2f}\n値下げあり {(x['値下げ回数'] > 0).mean() * 100:.0f}%", fontsize=9)
        ax.set_xlim(0, mx); ax.set_ylim(0, mx); ax.set_xlabel("初めて見たときの価格（万円・税込）")
        ax.set_title(a, loc="left", color=col, fontsize=13)
    axes[0].set_ylabel("消える直前の価格（万円・税込）")
    finish(fig, "消える直前の価格は、初めて見たときの価格よりどれだけ下がっていたか", src,
           os.path.join(ROOT, "charts", "16_消滅直前の価格.png"))
    log("図15・16を出力")


def survival(panel):
    """60・90・120・180日時点の残存率（観測で生年月日がその日齢を含む個体のうち、まだ掲載中の割合）。"""
    out = []
    last = panel["最終掲載日"].max()
    p = panel.copy()
    p["観測終わり日齢"] = p.apply(lambda r: r["消滅日齢"] if r["状態"] == "消滅" else r["現在日齢"], axis=1)
    def age_at(date, b):
        try:
            return (datetime.date.fromisoformat(date) - datetime.date.fromisoformat(b)).days
        except Exception:
            return None
    p["観測開始日齢"] = [age_at(f, b) for f, b in zip(p["初出日"], p["生年月日"])]
    for grp_col in [None, "チェーン名"]:
        for keys, g in (p.groupby(["動物"]) if grp_col is None else p.groupby(["動物", grp_col])):
            keys = keys if isinstance(keys, tuple) else (keys,)
            for age in [60, 90, 120, 180]:
                at_risk = g[(g["観測開始日齢"] <= age)]
                known = at_risk[(at_risk["観測終わり日齢"] >= age) | (at_risk["状態"] == "消滅")]
                if len(known) < 20:
                    continue
                alive = (known["観測終わり日齢"] >= age).mean()
                out.append(dict(動物=keys[0], チェーン=keys[1] if len(keys) > 1 else "全体", 日齢=age, 対象件数=len(known),
                                残存率=round(alive * 100, 1), 区分="計算", 計算日=last,
                                備考="観測開始時にその日齢以下だった個体のうち、その日齢まで掲載が続いた割合。観測期間が短いうちは過大"))
    pd.DataFrame(out).to_csv(os.path.join(PM, "残存率.csv"), index=False, encoding="utf-8-sig")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--init0", action="store_true")
    ap.add_argument("--force-charts", action="store_true")
    a = ap.parse_args()
    os.makedirs(SNAP, exist_ok=True)
    if a.init0 or not os.path.exists(os.path.join(SNAP, f"{BASE0}.csv")):
        init0()
    newly_gone, checked = [], []
    if not a.no_fetch:
        if not robots_ok():
            return 1
        prev_dates = sorted(load_snaps())
        prev = load_snaps()[prev_dates[-1]] if prev_dates else None
        ck_list = os.path.join(PM, f"_crawl_{TODAY}.csv")   # 途中保存（再起動で止まっても続きから）
        ck_det = os.path.join(PM, f"_checked_{TODAY}.csv")
        if os.path.exists(ck_list):
            df = pd.read_csv(ck_list, dtype={"個体ID": str})
            log(f"途中保存の一覧 {len(df):,}件を再利用（{TODAY}）")
        else:
            df = crawl()
            if len(df):
                df.to_csv(ck_list, index=False, encoding="utf-8-sig")
        if len(df) == 0:
            log("取得0件。サイト構造が変わった可能性。スナップショットは保存しない")
            return 1
        df["確認方法"] = "一覧"
        if prev is not None and prev_dates[-1] != TODAY:
            gone = prev[~prev["個体ID"].isin(df["個体ID"])]
            log(f"前回（{prev_dates[-1]}）にいて今回の一覧にいない個体 {len(gone):,}件 → 詳細ページを確認")
            rec = []
            done = {}
            if os.path.exists(ck_det):
                dd = pd.read_csv(ck_det, dtype={"個体ID": str})
                done = {x["個体ID"]: x for x in dd.to_dict("records")}
                log(f"途中保存の詳細確認 {len(done):,}件を再利用")
            for i, (_, r) in enumerate(gone.iterrows()):
                if r["個体ID"] in done:
                    x = done[r["個体ID"]]; st, price, code = x["確認結果"], x["詳細ページ価格"], x["HTTP"]
                else:
                    st, price, code = check_detail(r["掲載URL"])
                checked.append(st)
                rec.append(dict(個体ID=r["個体ID"], 確認日=TODAY, 確認結果=st, HTTP=code, 詳細ページ価格=price, 掲載URL=r["掲載URL"]))
                if st == "掲載継続（一覧で見落とし）":
                    keep = r.copy(); keep["取得日"] = TODAY; keep["価格"] = price; keep["確認方法"] = "詳細ページ（一覧で見落とし）"
                    df = pd.concat([df, keep.to_frame().T], ignore_index=True)
                else:
                    newly_gone.append(r["個体ID"])
                if (i + 1) % 200 == 0:
                    print(f"  詳細確認 {i + 1}/{len(gone)}", flush=True)
                    pd.DataFrame(rec).to_csv(ck_det, index=False, encoding="utf-8-sig")
            gp = os.path.join(PM, "disappeared.csv")
            pd.DataFrame(rec).to_csv(gp, mode="a", header=not os.path.exists(gp), index=False, encoding="utf-8-sig")
        df.to_csv(os.path.join(SNAP, f"{TODAY}.csv"), index=False, encoding="utf-8-sig")
        log(f"スナップショット保存 snapshots/{TODAY}.csv（{len(df):,}件）")
        for f in (ck_list, ck_det):
            if os.path.exists(f):
                os.remove(f)
    snaps = load_snaps()
    panel = build_panel(snaps)
    survival(panel)
    if not a.no_fetch and len(snaps) > 1:
        weekly_report(snaps, panel, newly_gone, checked)
    charts(panel, len(snaps), a.force_charts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
