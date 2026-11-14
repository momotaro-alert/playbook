#!/usr/bin/env python3
"""訂正の反映：petmi/_recheck.csv（再確認の結果）をスナップショット・disappeared.csv・panel・週報に反映する。
python3 -I work/petmi_recheck_apply.py"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import petmi_weekly as P

KEEP = "掲載継続（一覧で見落とし）"
rc = pd.read_csv(os.path.join(P.PM, "_recheck.csv"), dtype={"個体ID": str})
recheck_day = rc["再確認日"].max()
st = rc.set_index("個体ID")["確認結果"].to_dict()
ended = {k for k, v in st.items() if v not in (KEEP, "取得失敗")}
f03, f13 = os.path.join(P.SNAP, "2026-11-03.csv"), os.path.join(P.SNAP, "2026-11-13.csv")
s03 = pd.read_csv(f03, dtype={"個体ID": str}); s13 = pd.read_csv(f13, dtype={"個体ID": str})
miss03 = set(s03[s03["確認方法"].fillna("").str.contains("詳細ページ")]["個体ID"])
gone03 = ended & miss03          # 11-03 の時点で一覧に無かった → 11-03 に消えたものとして扱う
gone13 = ended - miss03
s03[~s03["個体ID"].isin(gone03)].to_csv(f03, index=False, encoding="utf-8-sig")
s13[~s13["個体ID"].isin(ended)].to_csv(f13, index=False, encoding="utf-8-sig")

gp = os.path.join(P.PM, "disappeared.csv")
g = pd.read_csv(gp, dtype={"個体ID": str})
if "備考" not in g.columns:
    g["備考"] = ""
g = g[~((g["確認日"] == "2026-11-13") & g["個体ID"].isin(ended))]
note = f"{recheck_day}の再確認で訂正（当初は『掲載が終了しました』の表示を拾えず掲載継続と誤判定）"
m = (g["確認日"] == "2026-11-03") & g["個体ID"].isin(gone03)
g.loc[m, "確認結果"] = g.loc[m, "個体ID"].map(st); g.loc[m, "備考"] = note
add = rc[rc["個体ID"].isin(gone13)].assign(確認日="2026-11-13", 備考=note)[["個体ID", "確認日", "確認結果", "HTTP", "詳細ページ価格", "掲載URL", "備考"]]
pd.concat([g, add], ignore_index=True).to_csv(gp, index=False, encoding="utf-8-sig")
P.log(f"訂正：再確認 {len(rc):,}件（{recheck_day}）→ 結果 {rc['確認結果'].value_counts().to_dict()}。"
      f"11-03 に消えた扱い {len(gone03):,}件、11-13 に消えた扱い {len(gone13):,}件をスナップショットから外した")

snaps = P.load_snaps(); panel = P.build_panel(snaps); P.survival(panel)
rp = os.path.join(P.PM, "report_weekly.md")
old = open(rp, encoding="utf-8").read()
head = old.split("\n## ")[0].rstrip()
os.rename(rp, os.path.join(P.PM, "report_weekly_訂正前.md"))
with open(rp, "w", encoding="utf-8") as f:
    f.write(head + f"\n\n> **訂正（{recheck_day}）**：2026-11-03 回と 2026-11-13 回の当初の週報は、詳細ページの「掲載が終了しました」という表示を拾えておらず、"
            "終了した個体を「掲載継続（一覧で見落とし）」と数えていた（当初の数字：11-03 犬0件・猫1件、11-13 犬12件・猫5件）。"
            f"該当する全件の詳細ページを {recheck_day} にもう一度確認し、下の数字に直した。当初の週報は report_weekly_訂正前.md に残している。"
            "11-03 回で「見落とし」とした個体のうち再確認で終了していたものは、11-03 の時点で一覧に無かったため 11-03 に消えたものとして数えた"
            "（実際に終了した日は 11-03〜11-13 のどこかで、特定できない）。"
            "「掲載が終了しました」は売れたのか取り下げたのかを示さない。\n")
dates = sorted(snaps)
g = pd.read_csv(gp, dtype={"個体ID": str})
for i in range(1, len(dates)):
    d = dates[i]; gd = g[g["確認日"] == d]
    gone_ids = gd[~gd["確認結果"].isin([KEEP, "取得失敗"])]["個体ID"].tolist()
    P.weekly_report({k: snaps[k] for k in dates[:i + 1]}, panel, gone_ids, gd["確認結果"].tolist())
P.charts(panel, len(snaps), False)
