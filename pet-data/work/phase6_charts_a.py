"""Phase6 前半: 図1,2,3,8,9 と H（立入検査）。"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from chartlib import *
from phase5_common import *

td = takedown()
ref, long_, yr = td["ref"], td["long"], td["yr"]
SRC1 = "環境省「犬・猫の引取り及び負傷動物等の収容並びに処分の状況」長期表(1974-2005)・参考表(2004-2024) " + ENV_DOGCAT + "（取得日 2026-11-02）"

# ---------- 図1 殺処分と引取りの長期推移 ----------
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4), sharey=True)
for ax, a, col, coll in [(axes[0], "犬", DOG, DOG_L), (axes[1], "猫", CAT, CAT_L)]:
    L = long_.loc[:2003]; R = ref
    ax.plot(L.index, L[(a, "引取り数")], color=coll, lw=2, label="引取り")
    ax.plot(L.index, L[(a, "殺処分数")], color=col, lw=2, label="殺処分")
    ax.plot(R.index, R[(a, "引取り数")], color=coll, lw=2)
    ax.plot(R.index, R[(a, "殺処分数")], color=col, lw=2)
    if a == "犬":
        ax.plot([2003, 2004], [L[(a, "引取り数")][2003], R[(a, "引取り数")][2004]], color=coll, lw=1, ls=":")
        ax.plot([2003, 2004], [L[(a, "殺処分数")][2003], R[(a, "殺処分数")][2004]], color=col, lw=1, ls=":")
        ax.annotate("2003年度以前の犬は\n野犬の捕獲（抑留）を含まない\n→実際はもっと多い", xy=(1990, 400000),
                    fontsize=8, color=INK2)
    ax.fill_between(R.index, R[(a, "殺処分数")], R[(a, "引取り数")], color=coll, alpha=0.25, lw=0)
    ax.set_title(a, loc="left", color=col, fontsize=13, fontweight="bold")
    ax.set_xlim(1973, 2026); ax.set_ylim(0, 600000)
    thousands(ax)
    t04, t24 = R[(a, "引取り数")][2004], R[(a, "引取り数")][2024]
    k04, k24 = R[(a, "殺処分数")][2004], R[(a, "殺処分数")][2024]
    ax.text(2024.5, t24 + 25000, f"2024年度\n引取り {t24:,.0f}\n殺処分 {k24:,.0f}", fontsize=8, ha="right", color=INK)
    ax.legend(loc="upper center", frameon=False, fontsize=9)
    events(ax, keys=[2013, 2019, 2021])
axes[0].set_ylabel("頭（年度）")
finish(fig, "殺処分は2004年度から98%減った。その92%は「引き取る数が91%減った」ことで説明できる",
       SRC1 + "。2004・2005年度の犬は抑留を勘案した推計値。薄い帯＝引き取ったが殺処分されなかった数（返還・譲渡・収容中など）",
       f"{CHARTS}/01_殺処分と引取りの長期推移.png")

# ---------- 図2 分類①②③ ----------
kc = rd("殺処分分類_全国.csv").drop_duplicates(["年", "動物", "項目"])
fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=False)
for ax, a, col in [(axes[0], "犬", DOG), (axes[1], "猫", CAT)]:
    x = kc[kc["動物"] == a].pivot_table(index="年", columns="項目", values="値")
    yrs = x.index.values
    b1, b2, b3 = x["殺処分数_①"], x["殺処分数_②"], x["殺処分数_③"]
    c1, c2, c3 = "#b9b8b2", col, "#5f5e5a"
    ax.bar(yrs, b2, color=c2, width=0.7, label="② それ以外（＝『殺処分ゼロ』の自治体が数えるもの）", edgecolor="#fcfcfb", lw=1.5)
    ax.bar(yrs, b1, bottom=b2, color=c1, width=0.7, label="① 譲渡に向かない（病気・攻撃性）", edgecolor="#fcfcfb", lw=1.5)
    ax.bar(yrs, b3, bottom=b1 + b2, color=c3, width=0.7, label="③ 収容後に死亡", edgecolor="#fcfcfb", lw=1.5)
    for y in yrs:
        ax.text(y, b1[y] + b2[y] + b3[y], f"{b1[y]+b2[y]+b3[y]:,.0f}", ha="center", va="bottom", fontsize=8)
        big = b2[y] > ax.get_ylim()[1] * 0.0 + (1200 if a == "犬" else 4000)
        ax.text(y, b2[y] / 2 if big else b2[y] + (40 if a == "犬" else 150), f"②{b2[y]:,.0f}", ha="center", va="center" if big else "bottom",
                fontsize=7.5, color="white" if big else INK)
    ax.set_title(a, loc="left", color=col, fontsize=13, fontweight="bold")
    thousands(ax); ax.set_xticks(yrs); ax.set_xticklabels([f"{y}" for y in yrs])
    ax.grid(axis="x", visible=False)
axes[1].legend(loc="upper right", frameon=False, fontsize=8)
axes[0].set_ylabel("頭（年度）")
finish(fig, "2024年度の殺処分6,830頭のうち、②「それ以外」はわずか892頭。①と③を外せば『ゼロ』に近づく",
       "環境省 事務提要（2018-2023年度は自治体別表の合計＝計算、2024年度は全国表）" + ENV_DOGCAT + "（取得日 2026-11-02）。負傷動物の処分は含まない",
       f"{CHARTS}/02_殺処分の分類内訳.png")

# ---------- 図3 業者数 ----------
bz = rd("動物取扱業_登録数_全国.csv").pivot_table(index="基準日", columns="項目", values="値", aggfunc="first")
bz.index = pd.to_datetime(bz.index)
xx = bz.index.year + (bz.index.dayofyear - 1) / 365
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
ax = axes[0]
ax.plot(xx, bz["第一種_総事業所数(実数)"], color=INK2, marker="o", ms=3.5, label="第一種（営利）総数")
ax.plot(xx, bz["第一種_販売"], color=GRAY, marker="o", ms=3.5, label="うち販売")
ax.plot(xx, bz["第一種_販売のうち犬猫等販売業"], color=DOG, marker="o", ms=3.5, label="うち犬猫等販売業")
ax.plot(xx, bz["第一種_犬猫等販売業のうち繁殖を行う者"], color=VIOLET, marker="o", ms=3.5, label="うち繁殖を行う者")
ax.set_ylim(0, 62000); thousands(ax); ax.set_xlim(2005.5, 2026)
ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=2); ax.set_ylabel("事業所（各年4月1日等の時点）")
ax.set_title("営利の業者", loc="left", fontsize=11)
events(ax, keys=[2013, 2019, 2021, 2024])
b25 = bz["第一種_犬猫等販売業のうち繁殖を行う者"].iloc[-1]
ax.annotate(f"繁殖業者 {b25:,.0f}\n数値規制の後も減っていない", xy=(xx[-1], b25), xytext=(2014.3, 4000), fontsize=8.5,
            arrowprops=dict(arrowstyle="-", color=GRAY, lw=0.8))
ax = axes[1]
ax.plot(xx, bz["第二種_総事業所数(実数)"], color=GREEN, marker="o", ms=3.5, label="第二種（非営利・保護団体等）総数")
ax.plot(xx, bz["第一種_譲受飼養業"], color=CAT, marker="o", ms=3.5, label="譲受飼養業（有料で引き取る業者）")
ax.plot(xx, bz["第一種_競りあっせん業"] * 10, color=GRAY, marker="o", ms=3.5, ls="--", label="競りあっせん業（オークション）×10")
ax.set_xlim(2005.5, 2026); thousands(ax)
ax.legend(frameon=False, fontsize=8.5, loc="upper left"); ax.set_title("受け皿側（2013年9月に新設）", loc="left", fontsize=11)
events(ax, keys=[2019, 2021, 2024])
for col, c in [("第二種_総事業所数(実数)", GREEN), ("第一種_譲受飼養業", CAT)]:
    v = bz[col].iloc[-1]; ax.text(xx[-1] + 0.2, v, f"{v:,.0f}", fontsize=8.5, color=INK, va="center")
for a_ in axes:
    a_.set_xticks(range(2006, 2026, 2)); a_.set_xticklabels([str(v) for v in range(2006, 2026, 2)])
finish(fig, "数値規制で「3割廃業」と言われた繁殖業者は13,347で横ばい。増えたのは保護団体（6.6倍）と引き取り業者（14.5倍）",
       "環境省 動物愛護管理行政事務提要「動物取扱業の登録・届出状況」" + ENV_BIZ + "（取得日 2026-11-02）。2006年3月は旧届出制。繁殖を行う者・第二種は2013年9月施行で新設、初回値は2014年4月。倍率は2014→2025年4月",
       f"{CHARTS}/03_動物取扱業の登録数.png")

# ---------- 図8 店頭価格 ----------
dt = rd("店頭価格_明細.csv")
dt = dt[(dt["生後日数"] >= 45) & (dt["生後日数"] <= 400)]
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4), sharey=True)
for ax, a, col, brs in [(axes[0], "犬", DOG, ["トイ・プードル", "チワワ", "ポメラニアン", "柴犬"]),
                         (axes[1], "猫", CAT, ["スコティッシュ・フォールド", "マンチカン", "ミヌエット", "ラグドール"])]:
    g = dt[dt["犬/猫"] == a]
    ax.scatter(g["生後日数"], g["価格"] / 10000, s=4, color=col, alpha=0.12, lw=0)
    bins = np.arange(45, 211, 15)
    styles = ["-", "--", "-.", ":"]
    for br, ls in zip(brs, styles):
        h = g[g["犬種/猫種"] == br]
        m = h.groupby(pd.cut(h["生後日数"], bins))["価格"].agg(["median", "size"])
        m = m[m["size"] >= 8]
        mid = [iv.mid for iv in m.index]
        ax.plot(mid, m["median"] / 10000, color=INK, lw=1.6, ls=ls, label=br)
    m = g.groupby(pd.cut(g["生後日数"], bins))["価格"].agg(["median", "size"]); m = m[m["size"] >= 8]
    ax.plot([iv.mid for iv in m.index], m["median"] / 10000, color=col, lw=3, label=f"{a}全体の中央値")
    ax.set_xlim(40, 215); ax.set_ylim(0, 80)
    ax.set_xlabel("生後日数（取得日−生年月日）")
    ax.set_title(a, loc="left", color=col, fontsize=13, fontweight="bold")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    n = len(g); old = (rd("店頭価格_明細.csv").query("`犬/猫`==@a")["生後日数"] > 180).mean() * 100
    ax.text(150, 62, f"掲載 {n:,} 件\n生後180日を超える掲載は {old:.0f}%", fontsize=8.5, color=INK2)
axes[0].set_ylabel("店頭価格（万円・税込）")
finish(fig, "店頭価格は生後60日から180日で犬74%・猫66%下がる。生後半年を過ぎた子は店頭からほぼ消える",
       "ペットミー掲載情報（https://petmi.jp/ 全国20品種 12,815件、取得日 2026-11-02）。同じ日の断面で、同じ個体を追ったものではない。点＝1件、線＝15日刻みの中央値（8件以上の区間のみ、生後210日まで。それ以上は件数が少なく特定チェーンの一律価格に偏るため描かない）",
       f"{CHARTS}/08_店頭価格の値下がり曲線.png")

# ---------- 図9 オークション ----------
fig, ax = plt.subplots(figsize=(10, 4.8))
labels = ["自称規模が分かる6会場の合計\n（主催者・紹介サイト／犬猫計）", "国の実数：19会場の直近1開催\n（2023年11月調査／犬のみ）"]
ax.barh([1, 0], [3287, 3800], color=[GRAY, DOG], height=0.5)
ax.barh([1], [3517 - 3287], left=[3287], color=GRAY, alpha=0.4, height=0.5)
ax.set_yticks([1, 0]); ax.set_yticklabels(labels)
ax.text(3530, 1, "3,287〜3,517頭/週", va="center", fontsize=10)
ax.text(3820, 0, "約3,800頭/週", va="center", fontsize=10)
ax.annotate("残り13会場に残るのは\n週513頭＝1会場あたり週39頭\n（自称が全部犬だった場合）", xy=(3550, 0.0), xytext=(4300, 0.55),
            fontsize=9, arrowprops=dict(arrowstyle="-", color=GRAY))
ax.set_xlim(0, 5600); thousands(ax, "x"); ax.set_xlabel("頭／週"); ax.grid(axis="y", visible=False)
finish(fig, "大手6会場の自称だけで国の実数の86%に達する。合うはずのない数字が、ほぼ合ってしまう",
       "環境省 ペットオークション一斉調査 https://www.env.go.jp/content/000199032.pdf ／ 自称規模は会場サイト・紹介サイト（二次）（取得日 2026-11-02）。落札価格は非公開。国は年換算で約19.8万頭（3,800×52、計算）",
       f"{CHARTS}/09_オークション自称vs実数.png")

# ---------- 図H 立入検査と処分 ----------
H = rd("計算_H_立入検査と処分.csv")
fig, ax = plt.subplots(figsize=(11, 4.8))
ax.bar(H["年"], H["立入検査件数"], color="#d9d8d2", width=0.7, label="立入検査件数（第一種）")
ax2y = H["処分等合計"]
for y, ins, act in zip(H["年"], H["立入検査件数"], ax2y):
    ax.text(y, ins + 400, f"{act:.0f}件", ha="center", fontsize=8.5, color=CAT if act else INK2, fontweight="bold")
thousands(ax); ax.set_ylabel("件（年度）"); ax.grid(axis="x", visible=False)
ax.set_xticks(H["年"])
ax.text(2011.6, 30500, "棒の上の数字＝その年の 勧告＋命令＋業務停止＋登録取消＋告発 の件数", fontsize=8.5, color=INK2)
ax.set_ylim(0, 32000)
events(ax, keys=[2013, 2019, 2021], ymax_frac=0.9)
finish(fig, "13年間で立入検査28万件、処分などは265件（0.09%）。オークション調査では調べた業者の約半数が違反",
       "環境省 事務提要「動物取扱業者に対する行政処分等の状況」" + ENV_ENF + "（取得日 2026-11-02）。口頭・文書の指導は統計に出ない。2012・2021・2023年度は東京都等の検査件数が全国計に入っていない（logs/phase1.md）。2023年度は措置命令31件",
       f"{CHARTS}/12_立入検査と処分.png")
print("ok")
