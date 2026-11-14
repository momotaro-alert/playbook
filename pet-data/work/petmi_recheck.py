#!/usr/bin/env python3
"""訂正用：『掲載継続（一覧で見落とし）』と判定した個体の詳細ページをもう一度確認する。
2026-11-13 回まで、詳細ページの「掲載が終了しました」という表示を拾えていなかった（判定の書き方の誤り）。
python3 -I work/petmi_recheck.py   # 途中保存あり。終了コード3なら同じコマンドで続きから
1リクエスト2秒以上・同時接続1（petmi_weekly.py の get をそのまま使う）。"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import petmi_weekly as P

T0 = time.time()
snap = pd.read_csv(os.path.join(P.SNAP, "2026-11-13.csv"), dtype={"個体ID": str})
todo = snap[snap["確認方法"] != "一覧"]
ck = os.path.join(P.PM, "_recheck.csv")
done = pd.read_csv(ck, dtype={"個体ID": str}).to_dict("records") if os.path.exists(ck) else []
seen = {x["個体ID"] for x in done}
if not seen and not P.robots_ok():
    sys.exit(1)
n = 0
for _, r in todo.iterrows():
    if r["個体ID"] in seen:
        continue
    st, price, code = P.check_detail(r["掲載URL"])
    done.append(dict(個体ID=r["個体ID"], 再確認日=P.TODAY, 確認結果=st, HTTP=code, 詳細ページ価格=price, 掲載URL=r["掲載URL"]))
    n += 1
    if n % 200 == 0:
        pd.DataFrame(done).to_csv(ck, index=False, encoding="utf-8-sig")
        print(f"  再確認 {len(done)}/{len(todo)}", flush=True)
        if time.time() - T0 > 95 * 60:
            print("時間切れ。同じコマンドで続きから"); sys.exit(3)
pd.DataFrame(done).to_csv(ck, index=False, encoding="utf-8-sig")
print("完了", len(done), pd.DataFrame(done)["確認結果"].value_counts().to_dict())
