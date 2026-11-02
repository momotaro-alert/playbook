"""ToUnicode を持たない CID TrueType フォントの PDF（ペットフード協会 2025年版等）からテキストを復元する。
埋め込みフォントの cmap(Unicode→GID) を逆引きし、CID(=GID, Identity) を Unicode へ戻す。
usage: python3 -I work/phase2_pdf_cid_text.py <in.pdf> <out.txt>
出力: ページごとに行を y 座標でまとめたテキスト
"""
import io, re, sys
import pdfplumber
from pypdf import PdfReader
from fontTools.ttLib import TTFont


def font_maps(path):
    rd = PdfReader(path)
    maps = {}
    for page in rd.pages:
        res = page.get('/Resources')
        if not res:
            continue
        res = res.get_object()
        fonts = res.get('/Font')
        stack = [res]
        # Form XObject 内のフォントも見る
        xo = res.get('/XObject')
        if xo:
            for k, v in xo.get_object().items():
                v = v.get_object()
                if v.get('/Resources'):
                    stack.append(v['/Resources'].get_object())
        for r in stack:
            fs = r.get('/Font')
            if not fs:
                continue
            for _, fref in fs.get_object().items():
                f = fref.get_object()
                base = str(f.get('/BaseFont', '')).lstrip('/')
                if base in maps:
                    continue
                desc = f.get('/DescendantFonts')
                if not desc:
                    continue
                d = desc.get_object()[0].get_object()
                fd = d.get('/FontDescriptor').get_object()
                ff = fd.get('/FontFile2')
                if not ff:
                    continue
                try:
                    tt = TTFont(io.BytesIO(ff.get_object().get_data()))
                    best = tt.getBestCmap() or {}
                except Exception:
                    best = {}
                inv = {}
                for u, gname in best.items():
                    gid = tt.getGlyphID(gname)
                    inv.setdefault(gid, chr(u))
                maps[base] = inv
    return maps


def main(src, dst):
    maps = font_maps(src)
    out = []
    with pdfplumber.open(src) as pdf:
        for i, pg in enumerate(pdf.pages, 1):
            lines = {}
            for c in pg.chars:
                t = c['text']
                m = re.fullmatch(r'\(cid:(\d+)\)', t)
                if m:
                    t = maps.get(c['fontname'], {}).get(int(m.group(1)), '�')
                key = round(c['top'] / 3)
                lines.setdefault(key, []).append((c['x0'], t, c['x1']))
            out.append(f'===== page {i} =====')
            for k in sorted(lines):
                cs = sorted(lines[k])
                s, last = '', None
                for x0, t, x1 in cs:
                    if last is not None and x0 - last > 4:
                        s += ' ' * max(1, int((x0 - last) / 4))
                    s += t
                    last = x1
                out.append(s)
    open(dst, 'w', encoding='utf-8').write('\n'.join(out))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
