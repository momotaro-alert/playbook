"""Phase6 後半: 図4,5,6,7,10,11,13,14。"""
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from chartlib import *
from phase5_common import *

PFURL = "ペットフード協会「全国犬猫飼育実態調査」https://petfood.or.jp/data/ （2023-2025年版、取得日 2026-11-02）"
D = rd("計算_D_頭数収支.csv")
pop = rd("飼育頭数_協会推計.csv")
pop = pop[pop["項目"] == "飼育頭数"]

# ---------- 図4 飼育頭数（旧式/新式）・新規・推計死亡 ----------
fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharex=True, gridspec_kw=dict(height_ratios=[1.3, 1]))
for j, (a, col, coll) in enumerate([("犬", DOG, DOG_L), ("猫", CAT, CAT_L)]):
    ax = axes[0, j]
    o = pop[(pop["動物"] == a) & pop["推計式"].str.startswith("旧式（全世帯")].set_index("年")["値"] / 10
    n = pop[(pop["動物"] == a) & pop["推計式"].str.startswith("新式")].set_index("年")["値"].sort_index() / 10
    ax.plot(o.index, o.values, color=coll, ls="--", marker="o", ms=4, label="旧式（発表当時の値）")
    ax.plot(n.index, n.values, color=col, marker="o", ms=4, label="新式（2021年改定、2013-20年は協会が遡及）")
    ax.set_ylim(0, 1400); ax.set_title(f"{a}：飼育頭数", loc="left", color=col, fontsize=12)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    events(ax, keys=[2013, 2019, 2021], ymax_frac=0.98)
    ax2 = axes[1, j]
    d = D[D["動物"] == a].set_index("年")
    ax2.bar(d.index - 0.2, d["新規飼育"] / 1e4, width=0.4, color=col, label="新規飼育（1年以内に飼い始めた）")
    ax2.bar(d.index + 0.2, d["推計死亡"] / 1e4, width=0.4, color=GRAY, label="推計死亡（飼育頭数÷平均寿命・計算）")
    ax2.set_ylim(0, 75); ax2.set_title(f"{a}：1年に増える数と減る数", loc="left", color=col, fontsize=12)
    ax2.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=2)
    gap = d.loc[2021:2025, "合わない頭数"].mean() / 1e4
    ax2.text(2007.6, 57, f"2021-25年平均：前年差−（新規−推計死亡）＝{gap:+.1f}万頭/年", fontsize=8.5, color=INK)
    ax2.set_xlim(2007.3, 2025.8); ax2.set_xticks(range(2008, 2026, 2)); ax2.set_xticklabels([str(v) for v in range(2008, 2026, 2)])
axes[0, 0].set_ylabel("万頭"); axes[1, 0].set_ylabel("万頭/年")
finish(fig, "犬は「新規＜死亡」で頭数が減り、数字がほぼ合う。猫は新規が死亡の7割しかないのに頭数が減らず、年20万頭が合わない",
       PFURL + "。旧式値は報道・日本獣医師会雑誌（二次）。旧式と新式は計算方法が違うので線をつながない。推計死亡は頭数が一定と仮定した目安",
       f"{CHARTS}/04_飼育頭数_新規_推計死亡.png")

# ---------- 図5 狂犬病登録 vs 協会推計 ----------
rb = rd("狂犬病_登録注射.csv")
reg = rb[rb["項目"] == "登録頭数"].drop_duplicates("年").set_index("年")["値"] / 1e4
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(reg.index, reg.values, color=INK2, lw=2, label="狂犬病予防法の登録頭数（厚労省）")
o = pop[(pop["動物"] == "犬") & pop["推計式"].str.startswith("旧式（全世帯")].set_index("年")["値"] / 10
n = pop[(pop["動物"] == "犬") & pop["推計式"].str.startswith("新式")].set_index("年")["値"].sort_index() / 10
ax.plot(o.index, o.values, color=DOG_L, ls="--", marker="o", ms=4, label="協会推計（旧式）")
ax.plot(n.index, n.values, color=DOG, marker="o", ms=4, label="協会推計（新式）")
for y, base, dy in [(2008, o, 40), (2013, o, 40), (2013, n, -90), (2025, n, 40)]:
    r = reg[y] / base[y] * 100
    ax.text(y, base[y] + dy, f"登録率{r:.0f}%", ha="center", fontsize=8.5, color=INK)
ax.set_xlim(1958, 2027); ax.set_ylim(0, 1400); ax.set_ylabel("万頭")
ax.legend(frameon=False, fontsize=9, loc="upper left")
events(ax, keys=[2013, 2019, 2022], ymax_frac=0.5)
ax.text(1961, 250, "猫には登録制度がないため、同じ比較はできない", fontsize=9, color=CAT)
finish(fig, "「犬の半分は未登録」は推計の計算式が生んだ数字。新しい式では登録率は88%",
       "厚生労働省 狂犬病予防法に基づく登録・注射頭数 https://www.mhlw.go.jp/bunya/kenkou/kekkaku-kansenshou10/02.html、e-Stat衛生行政報告例（2025年度）／" + PFURL + "。1996年までは暦年、1997年以降は年度。登録は死亡届が出ないと減らない",
       f"{CHARTS}/05_狂犬病登録と協会推計.png")

# ---------- 図6 業者の販売・死亡 vs 家庭の購入 ----------
B = rd("計算_B_業者販売と家庭購入.csv")
dl = rd("業者定期報告_販売死亡.csv")
fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), sharey=True)
for ax, a, col, coll in [(axes[0], "犬", DOG, DOG_L), (axes[1], "猫", CAT, CAT_L)]:
    b = B[B["動物"] == a].reset_index(drop=True)
    x = np.arange(len(b))
    ax.bar(x - 0.27, b["業者販売延べ"] / 1e4, width=0.26, color=coll, label="業者の販売・引渡し（延べ）")
    ax.bar(x, b["延べの半分"] / 1e4, width=0.26, color=col, label="同 ÷2（同じ子の二重計上を除く仮定）")
    ax.bar(x + 0.27, b["家庭の業者経由購入"] / 1e4, width=0.26, color=GRAY, label="家庭の業者経由購入（協会推計×構成比・計算）")
    for i, r in b.iterrows():
        dth = dl[(dl["年"] == r["年"]) & (dl["動物"] == a) & (dl["項目"] == "死亡数")]["値"].dropna()
        if len(dth):
            ax.text(i - 0.27, r["業者販売延べ"] / 1e4 + 1, f"死亡\n{dth.iloc[0]:,.0f}", ha="center", fontsize=7.5, color=INK2)
        ax.text(i + 0.27, r["家庭の業者経由購入"] / 1e4 + 1, f"{r['家庭の業者経由購入']/1e4:.1f}", ha="center", fontsize=7.5)
        ax.text(i, r["延べの半分"] / 1e4 + 1, f"{r['延べの半分']/1e4:.1f}", ha="center", fontsize=7.5)
    ax.set_xticks(x); ax.set_xticklabels([f"{int(y)}年度" for y in b["年"]])
    ax.set_title(a + ("（2016年度以降の犬の全国値は誰も集計していない）" if a == "犬" else "（2022年度は報道の『89%増』から逆算）"),
                 loc="left", color=col, fontsize=11)
    ax.legend(frameon=False, fontsize=8, loc="upper right"); ax.grid(axis="x", visible=False)
    ax.set_ylim(0, 95)
axes[0].set_ylabel("万頭")
finish(fig, "犬は業者の販売を半分にしても家庭の購入より年7〜8万頭多い。猫は業者販売が8年で1.9倍に増え、家庭の購入に追いついた",
       "業者の販売・死亡：犬猫等販売業者の定期報告を朝日新聞が全国集計した値（二次、clean/業者定期報告_販売死亡.csv）／家庭の購入：" + PFURL + "の新規飼育×『ショップ＋業者ブリーダー』の割合（2023-25年平均を過去に適用＝仮定）。死亡は死産・繁殖引退した親を含まない",
       f"{CHARTS}/06_業者販売と家庭購入.png")

# ---------- 図7 マイクロチップ純増 vs 購入 ----------
Cc = rd("計算_C_チップと購入.csv")
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
for ax, a, col, coll in [(axes[0], "犬", DOG, DOG_L), (axes[1], "猫", CAT, CAT_L)]:
    c = Cc[Cc["動物"] == a].reset_index(drop=True); x = np.arange(len(c))
    ax.bar(x - 0.27, c["MC純増"] / 1e4, width=0.26, color=col, label="マイクロチップ登録の純増（年度）")
    ax.bar(x, c["新規飼育"] / 1e4, width=0.26, color=coll, label="新規飼育（全経路）")
    ax.bar(x + 0.27, c["業者経由購入"] / 1e4, width=0.26, color=GRAY, label="うち業者経由（計算）")
    for i, r in c.iterrows():
        for dx, v in [(-0.27, r["MC純増"]), (0, r["新規飼育"]), (0.27, r["業者経由購入"])]:
            ax.text(i + dx, v / 1e4 + 0.8, f"{v/1e4:.1f}", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels([f"{int(y)}年度" for y in c["年"]])
    ax.set_title(a, loc="left", color=col, fontsize=13); ax.grid(axis="x", visible=False)
    ax.legend(frameon=False, fontsize=8, loc="upper right"); ax.set_ylim(0, 60)
axes[0].set_ylabel("万頭")
finish(fig, "犬のチップ登録は年43万頭増。業者から買われた子（31万頭）より年11万頭多く、新規飼育の全体とほぼ同じ",
       "環境省 マイクロチップ登録状況 " + ENV_MC + "／" + PFURL + "。登録義務は販売業者のみ（2022年6月〜）。純増は年度末累積の差。差分には繁殖用の親・売れ残り・家庭に届く前の死亡などが含まれうる（推測）",
       f"{CHARTS}/07_マイクロチップ純増と購入.png")

# ---------- 図13 死亡率の比較（犬・猫） ----------
DOGI = [
    ("国の公表値（2014年度）分母＝延べ販売、死産・親を除く", 2.9, DOG),
    ("同じ数字の分母を『実際の子の数』に直すと（計算）", 5.7, DOG),
    ("フランス繁殖場（犬20万頭）生きて生まれた子の生後2か月までの死亡（計算）", 6.5, GRAY),
    ("フランス繁殖場（犬）死産を含む", 13.4, GRAY),
    ("クーリク社 自社繁殖施設 2023年1-8月 死産含む（会社公表）", 18.4, INK2),
    ("クーリク社 内部資料とされる年平均（報道・二次）", 22.5, INK2),
    ("クーリク社 店舗段階（2023年）", 1.03, DOG_L),
]
CATI = [
    ("国の公表値（2014年度）分母＝延べ販売、死産・親を除く", 3.4, CAT),
    ("同じ数字の分母を『実際の子の数』に直すと（計算）", round(4664 / (133554 / 2 + 4664) * 100, 1), CAT),
    ("フランス繁殖場（猫2.8万頭）死産を除く離乳前の死亡", 8.2, GRAY),
    ("フランス繁殖場（猫）死産を含む離乳前の死亡", 16.0, GRAY),
    ("クーリク社 店舗段階（2023年）", 2.56, CAT_L),
]
fig, axes = plt.subplots(1, 2, figsize=(14, 5.6), gridspec_kw=dict(width_ratios=[1.35, 1]))
for ax, items, nm, col in [(axes[0], DOGI, "犬", DOG), (axes[1], CATI, "猫", CAT)]:
    y = np.arange(len(items))[::-1]
    ax.barh(y, [v for _, v, _ in items], color=[c for _, _, c in items], height=0.6)
    for yi, (lab, v, c) in zip(y, items):
        ax.text(v + 0.3, yi, f"{v:g}%", va="center", fontsize=9)
    ax.set_yticks(y); ax.set_yticklabels([textwrap.fill(l, 22) for l, _, _ in items], fontsize=8)
    ax.set_xlim(0, 26); ax.set_xlabel("死亡率（%）"); ax.grid(axis="y", visible=False)
    ax.set_title(nm, loc="left", color=col, fontsize=13)
finish(fig, "「死亡率1%前後」は店の段階だけの話。生まれてから店に出るまでを入れると、海外と同じく1〜2割が死んでいる",
       "環境省 中央環境審議会資料 https://www.env.go.jp/council/14animal/y140-42/900435217.pdf ／ フランスの繁殖場調査（犬204,537頭・猫28,065頭、PubMed抄録）／ Coo&RIKU・ペッツファースト公表資料 ／ デイリー新潮2023年8月30日（二次）（取得日 2026-11-02）。定義が違う数字を並べている点に注意。参考：ペッツファースト（犬猫）取扱頭数あたり0.68%（2024年）",
       f"{CHARTS}/13_死亡率の比較.png")

# ---------- 図14 猫の新規飼育の中身 ----------
src = rd("入手先構成.csv").pivot_table(index="項目", columns=["動物", "年"], values="値", aggfunc="first")
fig, ax = plt.subplots(figsize=(11, 5))
yrs = [2023, 2024, 2025]
parts = [("業者（ショップ＋業者ブリーダー）", ["ペットショップで購入", "業者のブリーダーから直接購入"], CAT),
         ("野良を拾った", ["野良犬・猫を拾った"], "#5f5e5a"),
         ("知人などから無償でもらった", ["友人/知人/親族からの無償譲渡"], "#b9b8b2"),
         ("保護団体・譲渡会・サイト（有償・無償）", ["シェルターからの有償譲渡・購入", "シェルターからの無償譲渡", "譲渡会を通じての無償譲渡（24年～）",
                                          "里親探しのマッチングサイトからの無償譲渡", "里親探しのマッチングサイトからの譲渡・購入"], GREEN)]
newc = D[D["動物"] == "猫"].set_index("年")["新規飼育"]
for i, y_ in enumerate(yrs):
    bot = 0
    for lab, keys, c in parts:
        v = sum(np.nan_to_num(src[("猫", y_)].get(f"入手先 {k}（1年以内飼育開始者）", 0)) for k in keys) / 100 * newc[y_] / 1e4
        ax.bar(i, v, bottom=bot, color=c, width=0.55, edgecolor="#fcfcfb", lw=1.5, label=lab if i == 0 else None)
        ax.text(i, bot + v / 2, f"{v:.1f}", ha="center", va="center", fontsize=8.5, color="white" if c in (CAT, "#5f5e5a", GREEN) else INK)
        bot += v
    dth = D[(D["動物"] == "猫") & (D["年"] == y_)]["推計死亡"].iloc[0] / 1e4
    ax.plot([i - 0.3, i + 0.3], [dth, dth], color=INK, lw=2)
    ax.text(i + 0.32, dth, f"推計死亡 {dth:.0f}万", va="center", fontsize=8)
ax.set_xticks(range(3)); ax.set_xticklabels([f"{y}年" for y in yrs]); ax.set_ylabel("万頭（1年以内に飼い始めた猫）")
ax.set_ylim(0, 75); ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=4); ax.grid(axis="x", visible=False)
finish(fig, "業者から来る猫は新しく飼われた猫の約3分の1（年12万頭）。野良・知人・保護団体からの猫がなければ、飼い猫の数は保てない",
       PFURL + "。入手先は複数回答の単純合計を新規飼育頭数に掛けた目安（計算）。『その他・ネット・自家繁殖』は省略",
       f"{CHARTS}/14_猫の新規飼育の入手先.png")


# ---------- 表画像（図10・図11） ----------
def table_png(rows, cols, widths, title, source, path, fs=8.5):
    wrapped = [[textwrap.fill(str(c), w) for c, w in zip(r, widths)] for r in rows]
    nlines = [max(c.count("\n") + 1 for c in r) for r in wrapped]
    hh = 0.22 * (sum(nlines) + 2) + 1.4
    fig, ax = plt.subplots(figsize=(14, hh))
    ax.axis("off")
    tb = ax.table(cellText=wrapped, colLabels=cols, colWidths=[w / sum(widths) for w in widths],
                  cellLoc="left", loc="upper center")
    tb.auto_set_font_size(False); tb.set_fontsize(fs)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor("#e6e5e0")
        if r == 0:
            cell.set_facecolor("#efeee9"); cell.set_height(0.3 / hh)
        else:
            cell.set_height((0.22 * nlines[r - 1] + 0.08) / hh)
            cell.set_facecolor("#fcfcfb")
    finish(fig, title, source, path)


S = [
    ["A", "殺処分−98%（犬猫）", "殺処分の減少の92%は『引取りが91%減った』で説明できる。2013年9月に飼い主・業者からの引取りを断れるようになり、飼い主からの引取りは2年で約半分に。2024年度の殺処分6,830頭のうち、②『それ以外』は892頭だけ。東京都・神奈川県は①と③を数えず『ゼロ』", "犬98.7%減/引取り90.4%減、猫98.0%/90.7%"],
    ["B", "需給ぴったり", "犬：業者の販売（延べ）を半分にしても、家庭が業者から買った数より年7〜8万頭多い。猫2014年度は逆に家庭の購入の方が多い（業者以外の供給が大きい）", "犬2014：30.9万 vs 22.5万"],
    ["C", "チップで全頭把握", "犬のチップ登録の純増（年43万）が、新規飼育の全体（40〜44万）とほぼ同じ。義務は業者経由の子だけなのに。業者経由の購入より年11万頭多い", "差 犬+11万/年、猫+5万/年"],
    ["D", "頭数は安定", "犬：新規42万−推計死亡47万で、実際に減っている（ずれ年6万）。猫：新規40万に対し推計死亡57万なのに頭数は横ばい→年21万頭が合わない", "猫の収支が合わない"],
    ["E", "犬の半分は未登録", "旧式の推計では登録率52%（2008年）。新式では88%（2025年）。『半分未登録』は推計式の産物。猫は登録制度がなく検証不能", "52%→88%"],
    ["F", "死亡率1%未満", "国の2.9%は分母が延べで死産を含まない。分母を直すと5.7%で、フランスの繁殖場（6.5%）と同じ水準。死産を含めると年約2.6万頭が数字に出ない（推測）。1%前後は店の段階だけ", "2.9%→5.7%、死産別"],
    ["G", "業者数は横ばい", "業界は数値規制で『犬の繁殖業者の32%が廃業』と警告。実際は2021→2025年で+2.3%（13,347）。増えたのは引き取り業者（205→290）と保護団体", "予想8,832 vs 実13,347"],
    ["H", "監視している", "2012-2024年度に立入検査28.4万件、勧告・命令・取消・告発などは265件（0.09%）。オークション調査で選んだ業者の約半数に違反", "0.09% vs 約50%"],
    ["I", "猫ブームに応えただけ", "猫の業者販売（延べ）は2014→2022年度で+89%、猫の新規飼育は+22%。需要の伸びを超えた業者販売は年約4.5万頭（推測）", "+89% vs +22%"],
    ["J", "猫も業者が供給", "猫の新規飼育の15〜24%は野良拾い。業者経由は約3分の1。野良拾いを除くと新規−推計死亡は年−27〜−29万", "業者は約12万頭/年"],
    ["K", "競りの規模", "大手6会場の自称（犬猫計 週3,287頭以上）だけで国の実数（犬 週3,800頭・19会場）の86%。残り13会場は週39頭ずつになる。国の調査は各会場1開催分で、週2回開く会場は少なく出る", "86%"],
    ["L", "売れ残りはいない", "店頭価格は生後60→180日で犬74%・猫66%下がる。掲載のうち生後180日を超えるのは犬6%・猫14%。その先の行き先は統計にない", "犬74%・猫66%下落"],
]
table_png(S, ["記号", "きれいに見える話", "数字を並べると（前提は clean/計算_*.csv）", "要点"], [4, 12, 70, 18],
          "「合ってはいけないのに合っている」「合うはずなのに合わない」12項目のまとめ",
          "pet-data/clean/計算_AFGHKL.csv、計算_BCDEFIJ.csv（計算日 2026-11-02）。各数字の出典URLは sources.md",
          f"{CHARTS}/10_AからLのまとめ.png")

M = rd("国が持っていない数字.csv")
table_png(M[["持っていない数字", "現状", "埋める方法（請求先・請求するもの）"]].values.tolist(),
          ["国が持っていない数字", "現状", "埋める方法（請求先・請求するもの）"], [22, 40, 48],
          "国が持っていない数字：生まれた数・死んだ理由・売れなかった子の行き先は、どこにも集計されていない",
          "pet-data/clean/国が持っていない数字.csv（2026-11-02時点の調査）", f"{CHARTS}/11_国が持っていない数字.png")
print("ok")
