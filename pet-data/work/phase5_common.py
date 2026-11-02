"""Phase5/6 共通: clean/ の読み込みと計算結果の書き出し。"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN = os.path.join(ROOT, "clean")
CHARTS = os.path.join(ROOT, "charts")
TODAY = "2026-11-02"

ENV_DOGCAT = "https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/dog-cat.html"
ENV_BIZ = "https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_1_1.pdf"
ENV_ENF = "https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_1_3.pdf"
ENV_MC = "https://www.env.go.jp/nature/dobutsu/aigo/2_data/statistics/files/r07/2_7.pdf"


def rd(name):
    return pd.read_csv(os.path.join(CLEAN, name))


def takedown():
    """全国の引取り・殺処分。2004年度以降は参考表(H16-R06)、それ以前は長期表(S49-H17)。"""
    d = rd("引取り処分_全国長期.csv")
    d = d[d["動物"].isin(["犬", "猫"])]
    out = {}
    for ser, key in [("参考表", "ref"), ("長期表", "long"), ("各年度版", "yr")]:
        x = d[d["系列"].astype(str).str.startswith(ser)]
        out[key] = x.pivot_table(index="年", columns=["動物", "項目"], values="値", aggfunc="first")
    return out


class Calc:
    """計算結果を1行ずつ貯めて CSV にする。"""

    def __init__(self):
        self.rows = []

    def add(self, 記号, 動物, 項目, 値, 単位, 計算式, 前提, 出典, 区分="計算"):
        self.rows.append(dict(計算記号=記号, 動物=動物, 項目=項目, 値=値, 単位=単位, 区分=区分,
                              計算式=計算式, 前提=前提, 使ったデータ=出典, 計算日=TODAY))

    def save(self, name):
        pd.DataFrame(self.rows).to_csv(os.path.join(CLEAN, name), index=False, encoding="utf-8-sig")
