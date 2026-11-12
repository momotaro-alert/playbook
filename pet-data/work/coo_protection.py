#!/usr/bin/env python3
"""Coo&RIKU「譲渡犬一覧」の取得（比較用）。一覧ページのみ（詳細ページには行かない）。
python3 -I work/coo_protection.py
1リクエスト3秒以上・同時接続1。robots.txt を確認。生HTMLは anifare/raw/coo_YYYY-MM-DD.tar.gz。
"""
import re, io, time, tarfile, datetime as dt
from pathlib import Path
import requests, pandas as pd
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "anifare" / "compare"
RAW = ROOT / "anifare" / "raw"
OUT.mkdir(parents=True, exist_ok=True); RAW.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0 (research; contact via site)"
JST = dt.timezone(dt.timedelta(hours=9))
TODAY = dt.datetime.now(JST).strftime("%Y-%m-%d")
BASE = "https://www.pet-coo.com"
LIST = BASE + "/protection/protection-dog/?tp=1&ord=date&cnt=120&pg={}&st=0&protect=1"
S = requests.Session(); S.headers["User-Agent"] = UA
raw = {}


def log(m):
    line = f"- {dt.datetime.now(JST).strftime('%Y-%m-%d %H:%M')} JST　[Coo&RIKU譲渡] {m}"
    print(line, flush=True)
    with open(ROOT / "anifare" / "log.md", "a", encoding="utf-8") as f:
        f.write(line + "\n")


def get(u, name):
    time.sleep(3.2)
    r = S.get(u, timeout=40)
    if r.status_code in (403, 429):
        log(f"{r.status_code}：ブロックとみなし中止"); raise SystemExit(2)
    raw[name] = r.content
    return r


r = get(BASE + "/robots.txt", "coo_robots.txt")
dis = [l.split(":", 1)[1].strip() for l in r.text.splitlines() if l.lower().startswith("disallow:")]
if any("/protection/".startswith(d) for d in dis if d):
    log(f"robots.txt で禁止 {dis} → 取得しない"); raise SystemExit(1)
log(f"robots.txt 確認：Disallow={dis}（/protection/ は対象外）")

rows, total, cum, pg = [], None, None, 1
while True:
    r = get(LIST.format(pg), f"coo_list_{pg}.html")
    s = BeautifulSoup(r.text, "html.parser")
    for x in s(["script", "style"]):
        x.decompose()
    t = s.get_text("\n", strip=True)
    if total is None:
        m = re.search(r"全\s*\n?\s*([\d,]+)\s*\n?\s*件", t); total = int(m.group(1).replace(",", "")) if m else None
        m = re.search(r"今までに\s*\n?\s*([\d,]+)\s*\n?\s*頭", t); cum = int(m.group(1).replace(",", "")) if m else None
        m = re.search(r"最新登録日は(\d{4}/\d{1,2}/\d{1,2})", t); latest = m.group(1) if m else ""
    parts = re.split(r"\n(No\.\d{6,10})\n", t)
    n0 = len(rows)
    for i in range(1, len(parts) - 1, 2):
        no, body = parts[i], parts[i + 1]
        lines = body.split("\n")
        breed = lines[0] if lines else ""
        b = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", body)
        sex = "オス" if "男の子" in body else ("メス" if "女の子" in body else "")
        shop = re.search(r"この子のいるお店\n([^\n]+)", body)
        par = re.search(r"両親の犬種\n母：([^\n]*)\n父：([^\n]*)", body)
        vac = re.search(r"予防接種\n：\n([^\n]+)", body)
        memo = re.search(r"性格・その他\n(.*?)\nこのワンちゃんを", body, re.S)
        rows.append({"掲載ID": no, "犬種": breed, "性別": sex,
                     "生年月日": f"{b.group(1)}-{int(b.group(2)):02d}-{int(b.group(3)):02d}" if b else "",
                     "店舗": shop.group(1) if shop else "", "両親の犬種": f"母:{par.group(1)} 父:{par.group(2)}" if par else "",
                     "予防接種": vac.group(1) if vac and vac.group(1) != "狂犬病予防接種" else "",
                     "性格・その他": memo.group(1).replace("\n", " ") if memo else "",
                     "出典URL": BASE + "/protection/protection-dog/", "取得日": TODAY})
    got = len(rows) - n0
    print(f"  page {pg}: {got}件", flush=True)
    if got == 0 or (total and len(rows) >= total) or pg >= 10:
        break
    pg += 1

df = pd.DataFrame(rows).drop_duplicates("掲載ID")
df["年齢_歳"] = [(pd.Timestamp(TODAY) - pd.Timestamp(b)).days / 365.25 if b else None for b in df["生年月日"]]
df.to_csv(OUT / f"coo_protection_{TODAY}.csv", index=False, encoding="utf-8-sig")
with tarfile.open(RAW / f"coo_{TODAY}.tar.gz", "w:gz") as tf:
    for n, b in raw.items():
        ti = tarfile.TarInfo(n); ti.size = len(b); ti.mtime = int(time.time()); tf.addfile(ti, io.BytesIO(b))
log(f"譲渡犬 {len(df)}頭を保存（サイト表示 全{total}件、累計『今までに{cum}頭の家族が決まりました』、最新登録日 {latest}）")
