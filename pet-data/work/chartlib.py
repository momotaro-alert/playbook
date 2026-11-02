"""グラフ共通部品。日本語フォント(IPAゴシック)を埋め込み、犬=青・猫=橙で固定。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import textwrap

FONT = "/usr/share/fonts/opentype/ipafont-gothic/ipagp.ttf"
fm.fontManager.addfont(FONT)
plt.rcParams.update({
    "font.family": fm.FontProperties(fname=FONT).get_name(),
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#8a8984", "axes.labelcolor": "#52514e",
    "xtick.color": "#52514e", "ytick.color": "#52514e",
    "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.8,
    "axes.axisbelow": True, "lines.linewidth": 2.0,
    "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb",
    "savefig.facecolor": "#fcfcfb", "font.size": 10.5,
})

DOG = "#2a78d6"      # 犬=青系
DOG_L = "#8fb8ea"    # 犬・淡
CAT = "#eb6834"      # 猫=橙系
CAT_L = "#f4ad8f"    # 猫・淡
GRAY = "#8a8984"
INK = "#0b0b0b"
INK2 = "#52514e"
GREEN = "#1baf7a"
VIOLET = "#6250d6"

# 注記線（制度の節目）。x は西暦の小数（年度グラフでは年度開始年基準の目安）
EVENTS = [
    (2013.75, "2013年9月\n引取り拒否可能に"),
    (2019.45, "2019年6月\n法改正"),
    (2021.45, "2021年6月\n数値規制施行"),
    (2022.45, "2022年6月\nチップ義務化"),
    (2024.45, "2024年6月\n数値規制完全施行"),
]


def events(ax, keys=None, ymax_frac=0.98, fontsize=7.5):
    """縦の注記線を入れる。keys で年を絞れる（例 [2013, 2019]）。"""
    lo, hi = ax.get_xlim()
    ytop = ax.get_ylim()[1]
    sel = [e for e in EVENTS if keys is None or int(e[0]) in keys]
    for i, (x, lab) in enumerate(sel):
        if not (lo <= x <= hi):
            continue
        ax.axvline(x, color=GRAY, lw=0.9, ls=(0, (3, 3)), zorder=1)
        ax.text(x, ytop * (ymax_frac - 0.11 * (i % 2)), lab, fontsize=fontsize,
                color=INK2, ha="left", va="top",
                bbox=dict(fc="#fcfcfb", ec="none", pad=0.5, alpha=0.85))


def finish(fig, title, source, path, subtitle=None):
    """タイトル=結論文、出典を図の下に小さく。"""
    fig.suptitle("\n".join(textwrap.wrap(title, 38)), x=0.02, ha="left",
                 fontsize=14, fontweight="bold", color=INK, y=0.995)
    if subtitle:
        fig.text(0.02, 0.905 if len(title) <= 38 else 0.865, subtitle,
                 fontsize=9.5, color=INK2, ha="left", va="top")
    fig.text(0.02, 0.01, "出典: " + source, fontsize=7, color=GRAY,
             ha="left", va="bottom", wrap=True)
    fig.savefig(path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def thousands(ax, axis="y", unit=""):
    import matplotlib.ticker as mt
    f = mt.FuncFormatter(lambda v, p: f"{v:,.0f}{unit}")
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(f)
