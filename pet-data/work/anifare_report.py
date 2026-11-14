#!/usr/bin/env python3
"""アニフェア調査：集計・図・CSV。python3 -I work/anifare_report.py"""
import sys, re
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from chartlib import DOG, DOG_L, CAT, GRAY, finish

ROOT = Path(__file__).resolve().parent.parent
AN = ROOT / "anifare"; OUT = AN / "clean"; CH = AN / "charts"
OUT.mkdir(exist_ok=True); CH.mkdir(exist_ok=True)
D = "2026-11-12"

# ---------- 1. 犬種ランキング（3つの出どころを同じ名前にそろえる） ----------
def norm(b):
    if re.search(r"×|MIX|ミックス|ハーフ", str(b)):
        return "ミックス"
    b = re.sub(r"[（(].*?[)）]", "", str(b)).replace("・", "").replace(" ", "")
    rules = [("トイプードル", "トイプードル"), ("チワワ", "チワワ"), ("カニーヘン|カニンヘン", "カニンヘンダックス"),
             ("ミニチュアダックス", "ミニチュアダックス"), ("ポメラニアン", "ポメラニアン"), ("マルチーズ", "マルチーズ"),
             ("シーズー", "シーズー"), ("ミニチュアシュナウザー", "ミニチュアシュナウザー"), ("豆柴", "豆柴"), ("柴", "柴犬"),
             ("フレンチブル", "フレンチブルドッグ"), ("ペキニーズ", "ペキニーズ"), ("パピヨン", "パピヨン"),
             ("ジャックラッセル", "ジャックラッセルテリア"), ("ボストンテリア", "ボストンテリア"), ("ミニチュアピンシャー", "ミニチュアピンシャー"),
             ("ヨークシャー", "ヨークシャーテリア"), ("ビションフリーゼ", "ビションフリーゼ"), ("ボーダーコリー", "ボーダーコリー"),
             ("キャバリア", "キャバリア"), ("パグ", "パグ"), ("イタリアングレー", "イタリアングレーハウンド"),
             ("MIX|ミックス|ハーフ|×", "ミックス")]
    for pat, name in rules:
        if re.search(pat, b):
            return name
    return b

# アニフェア：2026-11-12 トップページの「犬種から探す」に表示されていた頭数（1回閲覧。合計156）
ani_raw = {"アメリカン・コッカー・スパニエル": 1, "カニーヘンダックスフンド": 3, "キャバリアキングチャールズスパニエル": 1, "シーズー": 6,
           "ジャックラッセルテリア": 3, "チワワ": 22, "トイプードル": 35, "ハバニーズ": 1, "パグ": 1, "パピヨン": 3, "ビション・フリーゼ": 1,
           "フレンチ・ブルドッグ": 5, "ペキニーズ": 4, "ボストンテリア": 3, "ボーダーコリー": 2, "ポメラニアン": 16, "マルチーズ": 10,
           "ミニチュアシュナウザー": 5, "ミニチュアダックスフンド": 17, "ミニチュアピンシャー": 3, "ミニチュア・ブル・テリア": 1,
           "ヨークシャー・テリア": 1, "豆柴": 6, "ミックス犬": 6}
ani = pd.Series(ani_raw).groupby(norm).sum()
coo = pd.read_csv(AN / "compare" / f"coo_protection_{D}.csv")
coo_b = coo["犬種"].map(norm).value_counts()
pm = pd.read_csv(ROOT / "petmi" / "snapshots" / "2026-11-03.csv", dtype=str)
pm = pm[pm["動物"] == "犬"]
pm_b = pm["品種"].map(norm).value_counts()

rk = pd.DataFrame({"アニフェア_頭数": ani, "CooRIKU譲渡_頭数": coo_b, "ペットミー店頭_頭数": pm_b}).fillna(0).astype(int)
for c in list(rk.columns):
    rk[c.replace("頭数", "割合%")] = (rk[c] / rk[c].sum() * 100).round(1)
    rk[c.replace("頭数", "順位")] = rk[c].rank(ascending=False, method="min").astype(int)
rk = rk.sort_values("アニフェア_頭数", ascending=False)
rk.index.name = "犬種（そろえた名前）"
rk.to_csv(OUT / "犬種ランキング比較.csv", encoding="utf-8-sig")
top15 = rk.head(15)
# 一致度：アニフェア上位15のうち、店頭上位15にも入る数／順位相関（スピアマン、アニフェアに1頭以上いる犬種）
pm_top15 = set(rk.sort_values("ペットミー店頭_頭数", ascending=False).head(15).index)
coo_top15 = set(rk.sort_values("CooRIKU譲渡_頭数", ascending=False).head(15).index)
ov_pm = len(set(top15.index) & pm_top15); ov_coo = len(set(top15.index) & coo_top15)
sub = rk[rk["アニフェア_頭数"] > 0]
sp_pm = sub["アニフェア_頭数"].rank().corr(sub["ペットミー店頭_頭数"].rank())
sp_coo = sub["アニフェア_頭数"].rank().corr(sub["CooRIKU譲渡_頭数"].rank())
# 店頭上位15に入る犬種が、アニフェア掲載の何%を占めるか
share = rk.loc[list(pm_top15), "アニフェア_頭数"].sum() / rk["アニフェア_頭数"].sum() * 100

# ---------- 2. Coo&RIKU 譲渡犬：性別・年齢 ----------
coo["年齢_階級"] = np.floor(coo["年齢_歳"]).astype(int)
age = coo.groupby(["年齢_階級", "性別"]).size().unstack(fill_value=0)
age.to_csv(OUT / "CooRIKU譲渡_年齢1歳刻み.csv", encoding="utf-8-sig")
u1 = (coo["年齢_歳"] < 1).sum(); a24 = ((coo["年齢_歳"] >= 2) & (coo["年齢_歳"] < 4)).sum(); a48 = ((coo["年齢_歳"] >= 4) & (coo["年齢_歳"] < 8)).sum()
u6m = (coo["年齢_歳"] < 0.5).sum()
sex = coo["性別"].value_counts()
old = coo[coo["年齢_歳"] >= 4]; young = coo[coo["年齢_歳"] < 1]

# ---------- 3. アニフェア サイトマップ定点 ----------
panel = pd.read_csv(AN / "panel.csv", dtype=str).fillna("")
snaps = sorted((AN / "snapshots").glob("*.csv"))
flow = []
prev = None
for p in snaps:
    cur = set(pd.read_csv(p, dtype=str)["掲載ID"])
    flow.append({"取得日": p.stem, "掲載中": len(cur), "新規": len(cur - prev) if prev is not None else None,
                 "消えた": len(prev - cur) if prev is not None else None})
    prev = cur
flow = pd.DataFrame(flow); flow.to_csv(OUT / "アニフェア_掲載数の推移.csv", index=False, encoding="utf-8-sig")
# サイトマップの更新日時から見た「最後に更新されてからの日数」（掲載開始日ではない）
s0 = pd.read_csv(snaps[0], dtype=str)
lm = pd.to_datetime(s0["サイトマップ更新日時"].str[:10])
days_since = (pd.Timestamp(snaps[0].stem) - lm).dt.days
# 投稿IDの大きさ：新しく作られた順。最初の回の掲載のうち、IDが若い（古い）ものがどれだけ残っているか
ids = s0["掲載ID"].astype(int)

# ---------- 図 ----------
plt.rcParams["axes.unicode_minus"] = False
# 図A1 犬種
fig, ax = plt.subplots(figsize=(10, 6.2))
t = top15[::-1]; y = np.arange(len(t)); h = 0.27
ax.barh(y + h, t["アニフェア_割合%"], h, color=CAT, label=f"アニフェア掲載（{rk['アニフェア_頭数'].sum()}頭）")
ax.barh(y, t["CooRIKU譲渡_割合%"], h, color=DOG_L, label=f"Coo&RIKUの譲渡犬（{len(coo)}頭）")
ax.barh(y - h, t["ペットミー店頭_割合%"], h, color=DOG, label=f"ペットショップ店頭・ペットミー（{len(pm):,}頭）")
ax.set_yticks(y); ax.set_yticklabels(t.index); ax.set_xlabel("その場所の掲載全体に占める割合（%）"); ax.legend(loc="lower right", frameon=False)
ax.grid(axis="x", alpha=.25); [ax.spines[s].set_visible(False) for s in ("top", "right")]
finish(fig, f"アニフェアの上位15犬種のうち{ov_pm}犬種は、ペットショップ店頭の上位15犬種と同じ",
       "anifare.jp トップページの犬種別頭数（2026-11-12）、pet-coo.com 譲渡犬一覧（2026-11-12）、petmi.jp 全掲載（2026-11-03）。犬種名は表記をそろえた", CH / "A1_犬種ランキング比較.png")
# 図A2 Coo年齢
fig, ax = plt.subplots(figsize=(10, 5.2))
x = age.index.values
ax.bar(x - 0.2, age.get("メス", 0), 0.4, color=CAT, label=f"メス（{sex.get('メス', 0)}頭）")
ax.bar(x + 0.2, age.get("オス", 0), 0.4, color=DOG, label=f"オス（{sex.get('オス', 0)}頭）")
ax.set_xticks(x); ax.set_xticklabels([f"{i}歳" for i in x]); ax.set_ylabel("頭数"); ax.legend(frameon=False)
ax.grid(axis="y", alpha=.25); [ax.spines[s].set_visible(False) for s in ("top", "right")]
ax.annotate(f"1歳未満 {u1}頭（{u1 / len(coo) * 100:.0f}%）\nうち生後6か月未満 {u6m}頭", (0, age.loc[0].max()), (1.2, age.loc[0].max() * 0.9), fontsize=10, arrowprops=dict(arrowstyle="-", color=GRAY))
ax.annotate(f"4〜7歳 {a48}頭（{a48 / len(coo) * 100:.0f}%）", (5.5, age.loc[5].max()), (6.3, age.loc[5].max() * 1.5), fontsize=10, arrowprops=dict(arrowstyle="-", color=GRAY))
ax.annotate(f"2〜3歳は {a24}頭だけ", (2.5, 6), (2.0, age.loc[0].max() * 0.45), fontsize=10, arrowprops=dict(arrowstyle="-", color=GRAY))
finish(fig, "ペットショップ大手の「譲渡犬」は、子犬と4〜7歳の二つの山に分かれ、2〜3歳がほとんどいない",
       f"Coo&RIKU 譲渡犬一覧 https://www.pet-coo.com/protection/protection-dog/ （取得 2026-11-12、{len(coo)}頭、年齢は生年月日から計算）", CH / "A2_CooRIKU譲渡_年齢分布.png")
# 図A3 掲載数推移
fig, ax = plt.subplots(figsize=(9, 4.6))
xx = np.arange(len(flow))
ax.bar(xx, flow["掲載中"], 0.5, color=DOG_L, label="掲載中")
ax.bar(xx - 0.15, flow["新規"].fillna(0), 0.25, color=DOG, label="新しく載った")
ax.bar(xx + 0.15, flow["消えた"].fillna(0), 0.25, color=CAT, label="消えた")
for i, r in flow.iterrows():
    ax.text(i, r["掲載中"] + 2, f"{int(r['掲載中'])}頭", ha="center", fontsize=10)
    if pd.notna(r["新規"]):
        ax.text(i - 0.15, r["新規"] + 2, f"+{int(r['新規'])}", ha="center", fontsize=9, color=DOG)
        ax.text(i + 0.15, r["消えた"] + 2, f"−{int(r['消えた'])}", ha="center", fontsize=9, color=CAT)
ax.set_xticks(xx); ax.set_xticklabels(flow["取得日"]); ax.set_ylabel("頭数"); ax.legend(frameon=False, loc="center right")
ax.set_ylim(0, flow["掲載中"].max() * 1.2); [ax.spines[s].set_visible(False) for s in ("top", "right")]
finish(fig, f"アニフェアの掲載は常時150〜170頭。観測{len(flow)}回ではまだ傾向は言えない",
       "anifare.jp のサイトマップ（robots.txt が案内しているロボット向けファイル）。各日1回取得", CH / "A3_アニフェア掲載数の推移.png")

summary = dict(
    アニフェア掲載頭数_1112=int(rk["アニフェア_頭数"].sum()), 上位15の重なり_店頭=ov_pm, 上位15の重なり_Coo譲渡=ov_coo,
    順位相関_店頭=round(sp_pm, 2), 順位相関_Coo譲渡=round(sp_coo, 2), 店頭上位15犬種がアニフェアに占める割合=round(share, 1),
    Coo頭数=len(coo), Cooメス=int(sex.get("メス", 0)), Cooオス=int(sex.get("オス", 0)), Coo1歳未満=int(u1), Coo6か月未満=int(u6m),
    Coo2から3歳=int(a24), Coo4から7歳=int(a48), Coo年齢中央値=round(coo["年齢_歳"].median(), 2),
    Coo4歳以上のメス割合=round((old["性別"] == "メス").mean() * 100, 1), Coo4歳以上頭数=len(old),
    Coo1歳未満のメス割合=round((young["性別"] == "メス").mean() * 100, 1),
    サイトマップ更新から7日以内_1112=int((days_since <= 7).sum()), 同30日超=int((days_since > 30).sum()), 同最大日数=int(days_since.max()),
)
pd.Series(summary).to_csv(OUT / "集計サマリー.csv", header=["値"], encoding="utf-8-sig")
print(pd.Series(summary).to_string()); print(flow.to_string()); print(top15[["アニフェア_頭数", "アニフェア_割合%", "CooRIKU譲渡_割合%", "ペットミー店頭_割合%", "ペットミー店頭_順位"]].to_string())
