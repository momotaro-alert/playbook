"""report.md を、図を埋め込んだ1枚のHTML（report.html）にする。"""
import base64, os, re, markdown
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
md = open(os.path.join(ROOT, "report.md"), encoding="utf-8").read()
body = markdown.markdown(md, extensions=["tables", "sane_lists"])
def emb(m):
    p = os.path.join(ROOT, m.group(1))
    b = base64.b64encode(open(p, "rb").read()).decode()
    return f'src="data:image/png;base64,{b}"'
body = re.sub(r'src="(charts/[^"]+\.png)"', emb, body)
body = body.replace("<li>[x]", '<li class="ck">✅').replace("<li>[ ]", '<li class="ck">⬜')
css = """
:root{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--line:#e6e5e0;--card:#ffffff;--accent:#2a78d6;--th:#efeee9}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--line:#3a3a38;--card:#232322;--accent:#3987e5;--th:#2c2c2a}}
:root[data-theme="dark"]{--bg:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--line:#3a3a38;--card:#232322;--accent:#3987e5;--th:#2c2c2a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Hiragino Sans","Noto Sans JP","Yu Gothic",sans-serif;line-height:1.8;font-size:16px}
main{max-width:960px;margin:0 auto;padding:24px 16px 80px}
h1{font-size:1.7rem;line-height:1.4;margin:.4em 0 .2em}h2{font-size:1.3rem;margin-top:2.4em;padding-bottom:.3em;border-bottom:2px solid var(--line)}
h3{font-size:1.1rem;margin-top:2em;color:var(--accent)}p,li{color:var(--ink)}code{background:var(--th);padding:0 .3em;border-radius:4px;font-size:.9em}
img{width:100%;height:auto;border:1px solid var(--line);border-radius:8px;background:#fcfcfb;margin:.6em 0}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:.92rem;margin:1em 0}th,td{border:1px solid var(--line);padding:.45em .6em;text-align:left;vertical-align:top}th{background:var(--th)}
blockquote{margin:0;padding:.2em 1em;border-left:4px solid var(--line);color:var(--ink2)}hr{border:none;border-top:1px solid var(--line);margin:2em 0}
li.ck{list-style:none;margin-left:-1.2em}a{color:var(--accent)}
nav{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 16px;font-size:.85rem;overflow-x:auto;white-space:nowrap;z-index:2}
nav a{margin-right:1em;text-decoration:none}
"""
heads = re.findall(r"<h2>(.*?)</h2>", body)
for i, h in enumerate(heads):
    body = body.replace(f"<h2>{h}</h2>", f'<h2 id="s{i}">{h}</h2>', 1)
nav = "".join(f'<a href="#s{i}">{re.sub("<.*?>","",h)}</a>' for i, h in enumerate(heads))
body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
html = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ペット数字調査レポート</title><style>{css}</style></head><body><nav>{nav}</nav><main>{body}</main></body></html>"""
open(os.path.join(ROOT, "report.html"), "w", encoding="utf-8").write(html)
print(len(html) // 1024, "KB")
